import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parsers.srs_parser import srs_to_plantuml
from src.evaluators.semantic_eval import calculate_semantic_fidelity
from src.ocl_engine.ocl_validator import validate_ocl

# ── Test yardımcıları ──────────────────────────

ORNEK_SRS = """
The UserManager handles user authentication and registration.
The DiagramService generates PlantUML diagrams from SRS documents.
The ValidationEngine validates diagrams against OCL constraints.
The ReportGenerator creates PDF reports from evaluation results.
The UserManager uses the DiagramService to process uploaded documents.
"""

GECERLI_UML = """
@startuml
class UserManager {
    +login()
    +logout()
    +register()
}
class DiagramService {
    +generate()
}
class ValidationEngine {}
UserManager --> DiagramService
DiagramService --> ValidationEngine
@enduml
"""

GECERSIZ_UML = "class UserManager {}"  # @startuml/@enduml yok

# ── Parser Testleri ──────────────────────────

def test_parser_sinif_uretir():
    """Parser en az 1 sınıf üretmeli."""
    r = srs_to_plantuml(ORNEK_SRS)
    assert r["sinif_sayisi"] > 0, f"Sinif bulunamadi: {r}"
    print(f"  PASS: {r['sinif_sayisi']} sinif bulundu")

def test_parser_plantuml_etiketi():
    """Üretilen kod @startuml ve @enduml içermeli."""
    r = srs_to_plantuml(ORNEK_SRS)
    assert "@startuml" in r["plantuml_kodu"], "@startuml eksik"
    assert "@enduml" in r["plantuml_kodu"], "@enduml eksik"
    print("  PASS: PlantUML etiketleri mevcut")

def test_parser_bos_metin():
    """Boş metin hata vermemeli, hata alanı dolu olmalı."""
    r = srs_to_plantuml("")
    assert "hata" in r, "Hata alani yok"
    assert r["hata"] is not None, "Bos metin icin hata bekleniyor"
    print("  PASS: Bos metin durumu dogru islendi")

def test_parser_kisa_metin():
    """Çok kısa metin handle edilmeli."""
    r = srs_to_plantuml("abc")
    assert r["sinif_sayisi"] == 0 or r["hata"] is not None
    print("  PASS: Kisa metin durumu islendi")

# ── OCL Testleri ──────────────────────────

def test_ocl_gecerli_diyagram():
    """Geçerli UML kodu OCL testini geçmeli."""
    r = validate_ocl(GECERLI_UML)
    assert r["gecerli_mi"] == True, f"Hatalar: {r['hatalar']}"
    assert r["skor"] > 0.8, f"Skor cok dusuk: {r['skor']}"
    print(f"  PASS: Gecerli diyagram skor={r['yuzde']}")

def test_ocl_eksik_etiket():
    """@startuml eksikse hata vermeli."""
    r = validate_ocl(GECERSIZ_UML)
    assert r["gecerli_mi"] == False, "Eksik etiket tespit edilmedi"
    assert len(r["hatalar"]) > 0
    print(f"  PASS: Eksik etiket tespit edildi: {r['hatalar']}")

def test_ocl_bos_diyagram():
    """Boş diyagram hata vermeli."""
    r = validate_ocl("@startuml\n@enduml")
    assert r["sinif_sayisi"] == 0
    print(f"  PASS: Bos diyagram islendi, sinif_sayisi={r['sinif_sayisi']}")

# ── Semantik Değerlendirme Testleri ──────────────────────────

def test_semantik_yuksek_skor():
    """SRS ile eşleşen UML yüksek skor almalı."""
    srs = "UserManager handles authentication. DiagramService generates diagrams."
    uml = "@startuml\nclass UserManager {}\nclass DiagramService {}\nUserManager --> DiagramService\n@enduml"
    r = calculate_semantic_fidelity(srs, uml)
    assert r["genel_skor"] > 0.5, f"Skor beklenenden dusuk: {r['genel_skor']}"
    print(f"  PASS: Yuksek eslesme skoru={r['yuzde']}")

def test_semantik_halusinasyon():
    """UML'deki uydurma sınıflar halüsinasyon olarak işaretlenmeli."""
    srs = "UserManager handles users."
    uml = "@startuml\nclass UserManager {}\nclass UydurmaKlasFake {}\n@enduml"
    r = calculate_semantic_fidelity(srs, uml)
    assert len(r["halusinasyonlar"]) > 0, "Halusin. tespit edilmedi"
    print(f"  PASS: Halusinasyon tespit edildi: {r['halusinasyonlar']}")

def test_semantik_ieee_kriterleri():
    """IEEE kriterleri 4 kategori içermeli."""
    r = calculate_semantic_fidelity(ORNEK_SRS, GECERLI_UML)
    kriterler = r["ieee_kriterleri"]
    assert "C1_sinif_dogrul" in str(kriterler), "C1 kriteri eksik"
    assert "C2_iliski" in str(kriterler), "C2 kriteri eksik"
    assert "C3_butunluk" in str(kriterler), "C3 kriteri eksik"
    assert "C4_tutarlilik" in str(kriterler), "C4 kriteri eksik"
    print(f"  PASS: IEEE kriterleri mevcut: {list(kriterler.keys())}")

# ── Ana test koşucu ──────────────────────────

if __name__ == "__main__":
    testler = [
        ("Parser: Sinif uretimi", test_parser_sinif_uretir),
        ("Parser: PlantUML etiketleri", test_parser_plantuml_etiketi),
        ("Parser: Bos metin", test_parser_bos_metin),
        ("Parser: Kisa metin", test_parser_kisa_metin),
        ("OCL: Gecerli diyagram", test_ocl_gecerli_diyagram),
        ("OCL: Eksik etiket", test_ocl_eksik_etiket),
        ("OCL: Bos diyagram", test_ocl_bos_diyagram),
        ("Semantik: Yuksek skor", test_semantik_yuksek_skor),
        ("Semantik: Halusin. tespiti", test_semantik_halusinasyon),
        ("Semantik: IEEE kriterleri", test_semantik_ieee_kriterleri),
    ]
    
    gecti = 0
    kaldi = 0
    print("=" * 50)
    print("CURE Backend Test Paketi")
    print("=" * 50)
    for isim, test_fn in testler:
        print(f"\n[TEST] {isim}")
        try:
            test_fn()
            gecti += 1
        except Exception as e:
            print(f"  FAIL: {e}")
            kaldi += 1
    
    print("\n" + "=" * 50)
    print(f"Sonuc: {gecti}/{len(testler)} test gecti")
    if kaldi == 0:
        print("Tum testler basarili!")
    else:
        print(f"{kaldi} test basarisiz!")
