"""
CP2 - Hata isleme ve dogrulama yardimcilari.
AI/validator ciktilarini tek tip JSON formata cevirir ve runtime hatalarini loglar.
"""
import json
import re
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger("cure.error_handler")


# Frontend hata panelinin ayni kategorilerle calisabilmesi icin standart hata sozlugu.
HATA_KATEGORILERI = {
    "SYNTAX": "PlantUML sozdizimi hatasi",
    "OCL": "OCL kural ihlali",
    "SEMANTIC": "Semantik tutarsizlik",
    "HALLUCINATION": "Hallusinasyon tespit edildi",
    "MISSING_CLASS": "Eksik sinif",
    "PARSE": "Parser hatasi",
    "UNKNOWN": "Bilinmeyen hata"
}


def json_hata_parse_et(ham_json: str) -> dict:
    """
    AI hata raporu JSON'unu ayrikar.
    Duz JSON, markdown code block ve kismi key-value formatlarini tolere eder.
    """
    try:
        return json.loads(ham_json)
    except json.JSONDecodeError:
        pass

    # LLM bazen JSON'u ```json ... ``` icinde doner; once bu sarimi temizleriz.
    temiz = re.sub(r'```json\s*|\s*```', '', ham_json).strip()
    try:
        return json.loads(temiz)
    except json.JSONDecodeError:
        pass

    # JSON tamamen bozuksa en azindan "key: value" satirlarini kurtarmaya calisiriz.
    sonuc = {}
    for satir in ham_json.splitlines():
        eslesme = re.match(r'\s*"?(\w+)"?\s*:\s*"?([^",\n]+)"?', satir)
        if eslesme:
            sonuc[eslesme.group(1)] = eslesme.group(2).strip()

    if sonuc:
        logger.warning("JSON tam parse edilemedi, kismi kurtarma yapildi")
        return sonuc

    logger.error(f"JSON parse tamamen basarisiz: {ham_json[:100]}")
    return {"hata": "JSON parse edilemedi", "ham": ham_json[:200]}


def hata_normalize_et(hata_listesi: list, kaynak: str = "OCL") -> list:
    """
    Farkli kaynaklardan gelen hata listelerini tek standart response modeline cevirir.
    Bu sayede frontend hem syntax hem OCL hem semantic hatalari ayni sekilde gosterebilir.
    """
    normalize_edilmis = []
    for hata in hata_listesi:
        if isinstance(hata, str):
            kategori = "OCL" if "OCL" in hata.upper() else \
                       "SYNTAX" if any(k in hata.lower() for k in ["startuml", "enduml", "sozdizim"]) else \
                       "SEMANTIC" if any(k in hata.lower() for k in ["semantik", "hallusin", "eksik"]) else \
                       "UNKNOWN"
            normalize_edilmis.append({
                "mesaj": hata,
                "kategori": kategori,
                "aciklama": HATA_KATEGORILERI.get(kategori, ""),
                "kaynak": kaynak,
                "zaman": datetime.now().isoformat()
            })
        elif isinstance(hata, dict):
            hata.setdefault("kaynak", kaynak)
            hata.setdefault("zaman", datetime.now().isoformat())
            normalize_edilmis.append(hata)

    return normalize_edilmis


def exception_logla(exc: Exception, baglam: str = "") -> dict:
    """Runtime exception'lari standart log formatina cevirir."""
    hata_kaydi = {
        "tip": type(exc).__name__,
        "mesaj": str(exc),
        "baglam": baglam,
        "zaman": datetime.now().isoformat()
    }
    logger.error(f"[{baglam}] {type(exc).__name__}: {exc}")
    return hata_kaydi


def plantuml_syntax_kontrol(plantuml_kodu: str) -> dict:
    """
    PlantUML syntax on kontrolu.
    OCL validator'dan once temel etiket, sinif ve suslu parantez hatalarini yakalar.
    """
    hatalar = []

    if "@startuml" not in plantuml_kodu:
        hatalar.append("@startuml etiketi eksik")
    if "@enduml" not in plantuml_kodu:
        hatalar.append("@enduml etiketi eksik")

    siniflar = re.findall(r'class\s+(\w+)', plantuml_kodu)
    if not siniflar:
        hatalar.append("Hic sinif tanimlanmamis")

    acan = plantuml_kodu.count('{')
    kapanan = plantuml_kodu.count('}')
    if acan != kapanan:
        hatalar.append(f"Eslesmeyen suslu parantez: {acan} acik, {kapanan} kapali")

    return {
        "gecerli": len(hatalar) == 0,
        "hatalar": hatalar,
        "sinif_sayisi": len(siniflar)
    }


if __name__ == "__main__":
    ornek_json = '{"hata": "OCL-03", "aciklama": "Sinif bulunamadi", "siddet": "HATA"}'
    print("JSON parse:", json_hata_parse_et(ornek_json))

    hatalar = ["@startuml etiketi eksik", "Izole sinif: UserManager"]
    print("Normalize:", hata_normalize_et(hatalar))

    try:
        raise ValueError("Test exception")
    except Exception as e:
        print("Exception log:", exception_logla(e, "test_baglam"))
