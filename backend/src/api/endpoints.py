from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import sys, os, time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'ai_core', 'src'))
from parsers.srs_parser import srs_to_plantuml
from evaluators.semantic_eval import calculate_semantic_fidelity
from ocl_engine.ocl_validator import validate_ocl
from ocl_engine.error_handler import hata_normalize_et, plantuml_syntax_kontrol, exception_logla
from renderers.plantuml_renderer import render_plantuml
from plantuml_runtime import validate_with_plantuml
from api.error_log_endpoint import router as error_log_router, hata_kaydet, HataLogGirdisi
from api.performance import olcum_kaydet, performans_raporu, olcumleri_sifirla
from ai.agent_workflow import UMLMultiAgentSystem

# FastAPI uygulamasinin ana giris noktasi.
# Swagger ekraninda gorunen tum backend endpointleri bu app uzerinden yayinlanir.
app = FastAPI(
    title="CURE Backend API",
    description="Cognitive UML Repair Engine - Backend Services",
    version="1.0.0"
)

# Frontend farkli porttan calisabilecegi icin CORS acik tutulur.
# Boylece React/Vue arayuzu tarayici uzerinden bu API'ye istek atabilir.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hata log endpointleri ayri dosyada tutulur, burada ana API'ye baglanir.
app.include_router(error_log_router)


# Request modelleri: Gelen JSON verisini dogrular ve Swagger schema'sini olusturur.
class SRSGirdisi(BaseModel):
    # Kullanici/frontend gereksinim metnini bu alanla gonderir.
    metin: str = Field(..., min_length=10, description="SRS belgesi metni")
    dil: str = Field(default="en", description="Metin dili (en/tr)")


class UMLDogrulamaGirdisi(BaseModel):
    # Render, validate ve compile test endpointlerinde kullanilan PlantUML girdisi.
    plantuml_kodu: str = Field(..., description="Dogrulanacak PlantUML kodu")


class TamAnalizGirdisi(BaseModel):
    # Semantik karsilastirma icin kaynak SRS ve mevcut UML birlikte alinir.
    srs_metni: str = Field(..., min_length=10, description="SRS metni")
    plantuml_kodu: Optional[str] = Field(None, description="Varsa mevcut PlantUML")


class IterasyonGirdisi(BaseModel):
    # Her onarim denemesinde compile ve semantik test icin kullanilir.
    plantuml_kodu: str = Field(..., description="Test edilecek PlantUML kodu")
    iterasyon_no: int = Field(default=1, ge=1, le=3, description="Kacinci iterasyon (1-3)")
    srs_metni: Optional[str] = Field(None, description="Semantik degerlendirme icin SRS")


class AutonomousRepairRequest(BaseModel):
    # Max iterasyon 3 ile sinirli; bu sonsuz dongu riskini engeller.
    plantuml_kodu: str = Field(..., description="Onarilacak PlantUML kodu")
    srs_metni: Optional[str] = Field(None, description="Final semantik skor icin SRS metni")
    max_iterations: int = Field(default=3, ge=1, le=5, description="Guvenli maksimum iterasyon")


class PerformansOlcumGirdisi(BaseModel):
    # CP4 icin endpoint bazli latency ve basari olcumlerini kaydeder.
    endpoint: str = Field(..., description="Olculen endpoint")
    sure_saniye: float = Field(..., ge=0, description="Cagri suresi")
    basarili: bool = Field(default=True, description="Cagri basarili mi")


@app.get("/")
def ana_sayfa():
    return {
        "servis": "CURE Backend API",
        "versiyon": "1.0.0",
        "durum": "aktif",
        "endpoints": [
            "/generate-uml", "/api/parse", "/api/render", "/api/validate",
            "/api/evaluate", "/api/analyze", "/api/iterate",
            "/api/autonomous-repair", "/api/error-log", "/api/performance",
            "/api/demo-diagram", "/health"
        ]
    }


@app.get("/health")
def saglik_kontrolu():
    """Sunumda ilk gosterilecek endpoint: backend ayakta mi kontrol eder."""
    return {"durum": "aktif", "versiyon": "1.0.0"}


@app.get("/api/demo-diagram", response_class=HTMLResponse)
def demo_diagram_goster():
    """
    Sunum icin tarayicida dogrudan gorsel UML diyagrami gosterir.
    Swagger JSON response SVG'yi metin olarak gosterdigi icin bu endpoint HTML sayfasi dondurur.
    """
    ornek_metin = (
        "The UserManager handles user authentication. "
        "The DiagramService generates PlantUML diagrams. "
        "The UserManager uses the DiagramService."
    )
    sonuc = srs_to_plantuml(ornek_metin)
    render = render_plantuml(sonuc["plantuml_kodu"])
    return f"""
    <!doctype html>
    <html lang="tr">
      <head>
        <meta charset="utf-8">
        <title>CURE UML Demo Diagram</title>
        <style>
          body {{
            margin: 0;
            padding: 32px;
            font-family: Arial, sans-serif;
            background: #f8fafc;
            color: #0f172a;
          }}
          .panel {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border: 1px solid #dbe3ef;
            border-radius: 8px;
            padding: 24px;
          }}
          pre {{
            background: #0f172a;
            color: #e2e8f0;
            padding: 16px;
            border-radius: 6px;
            overflow: auto;
          }}
        </style>
      </head>
      <body>
        <div class="panel">
          <h1>CURE UML Demo Diagram</h1>
          <p>Bu sayfa backend'in urettigi PlantUML kodundan hazirlanan SVG diyagramini gorsel olarak gosterir.</p>
          {render["svg"]}
          <h2>Uretilen PlantUML</h2>
          <pre>{sonuc["plantuml_kodu"]}</pre>
        </div>
      </body>
    </html>
    """


def _basit_healer(plantuml_kodu: str) -> str:
    """
    Basit onarim katmani.
    Eksik @startuml/@enduml etiketlerini tamamlar ve bos diyagrami minimum sinifla doldurur.
    """
    kod = plantuml_kodu.strip()
    if "@startuml" not in kod:
        kod = "@startuml\n" + kod
    if "@enduml" not in kod:
        kod = kod + "\n@enduml"
    if "class " not in kod:
        kod = kod.replace("@enduml", "class GeneratedDiagram {}\n@enduml")
    return kod


def _compile_test(plantuml_kodu: str) -> dict:
    """
    CP3 compile test servisi.
    Once PlantUML syntax kontrolu, sonra OCL kurallari calisir; hatalar tek formata cevrilir.
    """
    syntax = plantuml_syntax_kontrol(plantuml_kodu)
    ocl = validate_ocl(plantuml_kodu)
    plantuml_runtime = validate_with_plantuml(plantuml_kodu)
    project_defined_success = syntax["gecerli"] and ocl["gecerli_mi"]
    plantuml_validated_success = (
        plantuml_runtime["successful"] if plantuml_runtime["available"] else None
    )
    hatalar = syntax["hatalar"] + ocl["hatalar"]
    if plantuml_runtime["available"] and plantuml_runtime["successful"] is False:
        hatalar.extend(plantuml_runtime["errors"])
    return {
        "basarili": project_defined_success,
        "success_definition": "project_defined_lightweight_validation",
        "project_defined_success": project_defined_success,
        "plantuml_validated_success": plantuml_validated_success,
        "plantuml_runtime_available": plantuml_runtime["available"],
        "syntax": syntax,
        "ocl": ocl,
        "plantuml_runtime": plantuml_runtime,
        "normalize_hatalar": hata_normalize_et(hatalar, kaynak="COMPILE")
    }


@app.post("/generate-uml")
def generate_uml(girdi: SRSGirdisi):
    """
    CP1 uyum endpointi.
    Frontend /generate-uml bekledigi icin asil /api/parse akisina yonlendirilir.
    """
    return srs_parse_et(girdi)


@app.post("/api/parse")
def srs_parse_et(girdi: SRSGirdisi):
    """SRS metnini PlantUML koduna cevirir, dogrular ve render cevabi ekler."""
    try:
        # 1) Gereksinim metninden siniflar ve iliskiler cikarilir.
        sonuc = srs_to_plantuml(girdi.metin)
        if sonuc.get("hata"):
            raise HTTPException(status_code=400, detail=sonuc["hata"])

        # 2) Uretilen PlantUML SVG/PNG response formatina cevrilir.
        render = render_plantuml(sonuc["plantuml_kodu"])

        # 3) UML, OCL kurallariyla dogrulanir ve ayni JSON cevabina eklenir.
        ocl_sonuc = validate_ocl(sonuc["plantuml_kodu"])
        cevap = {
            "basarili": True,
            "plantuml_kodu": sonuc["plantuml_kodu"],
            "siniflar": sonuc["bulunan_siniflar"],
            "iliskiler": sonuc["iliskiler"],
            "sinif_sayisi": sonuc["sinif_sayisi"],
            "render": render,
            "dogrulama": {
                "gecerli_mi": ocl_sonuc["gecerli_mi"],
                "hatalar": ocl_sonuc["hatalar"],
                "uyarilar": ocl_sonuc["uyarilar"],
                "skor": ocl_sonuc["skor"],
            },
            "response_format": "json"
        }
        olcum_kaydet("/api/parse", 0.0, True)
        return cevap
    except HTTPException:
        raise
    except Exception as e:
        exception_logla(e, "/api/parse")
        raise HTTPException(status_code=500, detail=f"Parser hatasi: {str(e)}")


@app.post("/api/render")
def plantuml_render_et(girdi: UMLDogrulamaGirdisi):
    """PlantUML kodunu SVG/PNG cevap formatina render eder."""
    try:
        # Render'dan once syntax kontrolu yapilir; hatali UML icin 400 response doner.
        compile_sonuc = _compile_test(girdi.plantuml_kodu)
        if not compile_sonuc["syntax"]["gecerli"]:
            raise HTTPException(status_code=400, detail=compile_sonuc["normalize_hatalar"])
        return {
            "basarili": True,
            "plantuml_kodu": girdi.plantuml_kodu,
            "render": render_plantuml(girdi.plantuml_kodu),
            "compile": compile_sonuc
        }
    except HTTPException:
        raise
    except Exception as e:
        exception_logla(e, "/api/render")
        raise HTTPException(status_code=500, detail=f"Render hatasi: {str(e)}")


@app.post("/api/validate")
def uml_dogrula(girdi: UMLDogrulamaGirdisi):
    """PlantUML kodunu OCL kurallarina gore dogrular."""
    try:
        sonuc = validate_ocl(girdi.plantuml_kodu)
        return {
            "basarili": True,
            "gecerli_mi": sonuc["gecerli_mi"],
            "skor": sonuc["skor"],
            "yuzde": sonuc["yuzde"],
            "hatalar": sonuc["hatalar"],
            "uyarilar": sonuc["uyarilar"],
            "sinif_sayisi": sonuc["sinif_sayisi"],
            "detaylar": sonuc["detaylar"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCL dogrulama hatasi: {str(e)}")


@app.post("/api/evaluate")
def semantik_degerlendir(girdi: TamAnalizGirdisi):
    """SRS metni ile PlantUML'i proje ici semantik kriterlere gore karsilastirir."""
    if not girdi.plantuml_kodu:
        raise HTTPException(status_code=400, detail="Degerlendirme icin plantuml_kodu gerekli")
    try:
        sonuc = calculate_semantic_fidelity(girdi.srs_metni, girdi.plantuml_kodu)
        return {
            "basarili": True,
            "genel_skor": sonuc["genel_skor"],
            "yuzde": sonuc["yuzde"],
            "gecti_mi": sonuc["gecti_mi"],
            "halusinasyonlar": sonuc["halusinasyonlar"],
            "eksik_siniflar": sonuc["eksik_siniflar"],
            "ieee_kriterleri": sonuc["ieee_kriterleri"],
            "sinif_metrikleri": sonuc["sinif_metrikleri"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Degerlendirme hatasi: {str(e)}")


@app.post("/api/iterate")
def iterasyon_testi(girdi: IterasyonGirdisi):
    """Her onarim iterasyonunda compile + opsiyonel semantik test calistirir."""
    MAX_ITERATIONS = 3
    if girdi.iterasyon_no > MAX_ITERATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Maksimum iterasyon sayisi aşıldı: {MAX_ITERATIONS}"
        )

    baslangic = time.time()

    try:
        compile_sonuc = _compile_test(girdi.plantuml_kodu)
        ocl_sonuc = compile_sonuc["ocl"]
        compile_basarili = compile_sonuc["basarili"]

        semantik_sonuc = None
        if girdi.srs_metni:
            semantik_sonuc = calculate_semantic_fidelity(girdi.srs_metni, girdi.plantuml_kodu)

        gecen_sure = round(time.time() - baslangic, 3)

        if compile_basarili and (semantik_sonuc is None or semantik_sonuc["gecti_mi"]):
            durum = "BASARILI"
        elif compile_basarili:
            durum = "COMPILE_OK_SEMANTIK_DUSUK"
        else:
            durum = "COMPILE_HATALI"

        return {
            "basarili": True,
            "iterasyon_no": girdi.iterasyon_no,
            "max_iterations": MAX_ITERATIONS,
            "son_iterasyon_mu": girdi.iterasyon_no >= MAX_ITERATIONS,
            "durum": durum,
            "compile": {
                "basarili": compile_basarili,
                "skor": ocl_sonuc["skor"],
                "yuzde": ocl_sonuc["yuzde"],
                "hatalar": ocl_sonuc["hatalar"],
                "uyarilar": ocl_sonuc["uyarilar"],
                "normalize_hatalar": compile_sonuc["normalize_hatalar"]
            },
            "semantik": {
                "genel_skor": semantik_sonuc["genel_skor"] if semantik_sonuc else None,
                "yuzde": semantik_sonuc["yuzde"] if semantik_sonuc else None,
                "gecti_mi": semantik_sonuc["gecti_mi"] if semantik_sonuc else None,
                "halusinasyonlar": semantik_sonuc["halusinasyonlar"] if semantik_sonuc else [],
            } if semantik_sonuc else None,
            "sure_saniye": gecen_sure
        }

    except HTTPException:
        raise
    except Exception as e:
        exception_logla(e, "/api/iterate")
        raise HTTPException(status_code=500, detail=f"Iterasyon test hatasi: {str(e)}")


@app.post("/api/autonomous-repair")
def autonomous_repair(girdi: AutonomousRepairRequest):
    """
    Gerçek AI (Healer/Critic) ajanını kullanan otonom onarım akışı.
    """
    baslangic = time.time()
    aktif_kod = girdi.plantuml_kodu
    
    # Başlangıç durumu kontrolü
    compile_sonuc = _compile_test(aktif_kod)
    iterasyonlar = []
    agent_iteration_count = None
    agent_repair_attempt_count = None
    agent_is_valid = None
    agent_llm_call_count = 0

    iterasyonlar.append({
        "iteration_no": 1,
        "status": "COMPILE_OK" if compile_sonuc["basarili"] else "HEALER_REQUIRED",
        "compile_result": compile_sonuc,
        "fix_summary": "İlk derleme testi (Orijinal UML)"
    })

    # Eğer kodda hata varsa, LangGraph AI Ajanını devreye sok
    if not compile_sonuc["basarili"]:
        try:
            # Multi-Agent sistemi başlatılıyor
            agent = UMLMultiAgentSystem(max_iterations=girdi.max_iterations)
            
            # Eğer SRS metni boş gelirse varsayılan bir prompt veriyoruz
            srs_metni = girdi.srs_metni if girdi.srs_metni else "Verilen UML kodunu OCL ve sözdizimi kurallarına uygun şekilde onar."
            
            # Ajan kendi içerisindeki 3 iterasyonluk döngüyü çalıştırıp en iyi sonucu döner
            aktif_kod = agent.run(original_text=srs_metni, initial_uml=aktif_kod)
            if agent.last_final_state:
                agent_repair_attempt_count = agent.last_final_state.get("repair_attempt_count")
                agent_iteration_count = agent_repair_attempt_count
                agent_is_valid = agent.last_final_state.get("is_valid")
            agent_llm_call_count = agent.llm_call_count
            
            # Ajanın çıktısı tekrar test ediliyor
            yeni_compile = _compile_test(aktif_kod)
            iterasyonlar.append({
                "iteration_no": 2,
                "status": "AI_HEALER_APPLIED",
                "compile_result": yeni_compile,
                "fix_summary": "LangGraph Multi-Agent sistemi ile otonom onarım uygulandı."
            })
            
            # Başarısızlık devam ediyorsa logla
            if not yeni_compile["basarili"]:
                hata_kaydet(HataLogGirdisi(
                    kategori="AI_HEALER_FAILED",
                    mesaj="Ajan onarımı sonrası hatalar devam ediyor: " + "; ".join(yeni_compile["syntax"]["hatalar"] or yeni_compile["ocl"]["hatalar"]),
                    plantuml_kodu=aktif_kod,
                    iterasyon_no=2,
                    skor=yeni_compile["ocl"]["skor"]
                ))
                
        except Exception as e:
            exception_logla(e, "/api/autonomous-repair - AI Ajan Hatası")

    # Final Değerlendirmeleri
    final_compile = _compile_test(aktif_kod)
    semantik = calculate_semantic_fidelity(girdi.srs_metni, aktif_kod) if girdi.srs_metni else None
    sure = round(time.time() - baslangic, 3)
    basarili = final_compile["basarili"]
    olcum_kaydet("/api/autonomous-repair", sure, basarili)

    return {
        "basarili": basarili,
        "sure_saniye": sure,
        "sla_gecti_mi": sure < 15,
        "max_iterations": girdi.max_iterations,
        "agent_iteration_count": agent_iteration_count,
        "agent_repair_attempt_count": agent_repair_attempt_count,
        "agent_is_valid": agent_is_valid,
        "agent_llm_call_count": agent_llm_call_count,
        "iterasyonlar": iterasyonlar,
        "final_plantuml": aktif_kod,
        "final_render": render_plantuml(aktif_kod) if basarili else None,
        "final_compile": final_compile,
        "semantik": semantik,
    }


@app.post("/api/analyze")
def tam_analiz_yap(girdi: SRSGirdisi):
    """Tam pipeline: SRS -> UML uret -> OCL dogrula -> semantik degerlendir."""
    baslangic = time.time()
    try:
        parse_sonuc = srs_to_plantuml(girdi.metin)
        if parse_sonuc.get("hata"):
            raise HTTPException(status_code=400, detail=parse_sonuc["hata"])

        uml = parse_sonuc["plantuml_kodu"]
        ocl_sonuc = validate_ocl(uml)
        eval_sonuc = calculate_semantic_fidelity(girdi.metin, uml)

        gecen_sure = round(time.time() - baslangic, 3)
        olcum_kaydet("/api/analyze", gecen_sure, True)

        return {
            "basarili": True,
            "sure_saniye": gecen_sure,
            "sla_gecti_mi": gecen_sure < 15,
            "uretilen_uml": uml,
            "siniflar": parse_sonuc["bulunan_siniflar"],
            "iliskiler": parse_sonuc["iliskiler"],
            "ocl": {
                "gecerli_mi": ocl_sonuc["gecerli_mi"],
                "skor": ocl_sonuc["skor"],
                "yuzde": ocl_sonuc["yuzde"],
                "hatalar": ocl_sonuc["hatalar"],
                "uyarilar": ocl_sonuc["uyarilar"]
            },
            "semantik": {
                "genel_skor": eval_sonuc["genel_skor"],
                "yuzde": eval_sonuc["yuzde"],
                "gecti_mi": eval_sonuc["gecti_mi"],
                "halusinasyonlar": eval_sonuc["halusinasyonlar"],
                "ieee_kriterleri": eval_sonuc["ieee_kriterleri"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        exception_logla(e, "/api/analyze")
        raise HTTPException(status_code=500, detail=f"Analiz hatasi: {str(e)}")


@app.post("/api/performance/measure")
def performans_olcum_kaydet(girdi: PerformansOlcumGirdisi):
    """Manuel performans olcumu eklemek icin kullanilir."""
    olcum_kaydet(girdi.endpoint, girdi.sure_saniye, girdi.basarili)
    return {"basarili": True, "mesaj": "Olcum kaydedildi"}


@app.get("/api/performance")
def performans_getir(endpoint: Optional[str] = None):
    """CP4 sunumunda P50/P95/P99 ve 15 saniye SLA sonucunu gosterir."""
    return performans_raporu(endpoint)


@app.delete("/api/performance")
def performans_temizle():
    olcumleri_sifirla()
    return {"basarili": True, "mesaj": "Performans olcumleri temizlendi"}
