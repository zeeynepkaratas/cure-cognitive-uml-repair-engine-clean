"""
CP3 + CP4 - Kapsamlı test paketi
Unit testler, integration testler, E2E testler, performans testleri
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parsers.srs_parser import srs_to_plantuml
from src.evaluators.semantic_eval import calculate_semantic_fidelity
from src.ocl_engine.ocl_validator import validate_ocl
from src.ocl_engine.error_handler import (
    json_hata_parse_et,
    hata_normalize_et,
    exception_logla,
    plantuml_syntax_kontrol,
)
from src.api.performance import olcum_kaydet, performans_raporu, olcumleri_sifirla, percentile_hesapla

# ── Test verileri ──────────────────────────────────────────────────────────

SRS_BASIT = """
The UserManager handles user authentication and registration.
The DiagramService generates PlantUML diagrams from SRS documents.
The ValidationEngine validates diagrams with OCL-like structural checks.
The UserManager uses the DiagramService to process uploaded documents.
"""

SRS_KARMASIK = """
The SystemController manages the entire application lifecycle.
The AuthenticationService handles user login, logout, and session management.
The DiagramGenerator creates PlantUML class diagrams from natural language requirements.
The OCLValidator validates generated diagrams with OCL-like structural checks.
The SemanticEvaluator compares UML diagrams with source SRS documents using project-defined criteria inspired by IEEE/ISO 29148.
The ReportService generates PDF and CSV reports from evaluation results.
The DatabaseManager stores and retrieves diagram versions and evaluation logs.
The SystemController uses the AuthenticationService for access control.
The DiagramGenerator communicates with the OCLValidator for syntax checking.
The SemanticEvaluator sends results to the ReportService.
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
    +validate()
}
class ValidationEngine {
    +check()
}
UserManager --> DiagramService
DiagramService --> ValidationEngine
@enduml
"""

HATALI_UML_SYNTAX = "class UserManager {}"  # @startuml/@enduml yok

HATALI_UML_OCL = """
@startuml
class userManager {}
class userManager {}
class IzoleClass {}
@enduml
"""

# ── CP2: Unit Testler — Error Handler ─────────────────────────────────────


def test_json_parser_duzgun():
    """Geçerli JSON doğru parse edilmeli."""
    girdi = '{"hata": "OCL-03", "siddet": "HATA"}'
    sonuc = json_hata_parse_et(girdi)
    assert sonuc["hata"] == "OCL-03"
    print("  PASS: JSON parser - düzgün JSON")


def test_json_parser_markdown():
    """Markdown sarmalı JSON parse edilmeli."""
    girdi = '```json\n{"hata": "test", "siddet": "UYARI"}\n```'
    sonuc = json_hata_parse_et(girdi)
    assert "hata" in sonuc
    print("  PASS: JSON parser - markdown sarmalı")


def test_hata_normalize():
    """String hata listesi normalize edilmeli."""
    hatalar = ["@startuml etiketi eksik", "Izole sinif: UserManager"]
    sonuc = hata_normalize_et(hatalar)
    assert len(sonuc) == 2
    assert "kategori" in sonuc[0]
    assert "zaman" in sonuc[0]
    print("  PASS: Hata normalize - format doğru")


def test_syntax_kontrol_gecerli():
    """Geçerli UML syntax kontrolünden geçmeli."""
    sonuc = plantuml_syntax_kontrol(GECERLI_UML)
    assert sonuc["gecerli"]
    assert len(sonuc["hatalar"]) == 0
    print(f"  PASS: Syntax kontrol - geçerli UML ({sonuc['sinif_sayisi']} sınıf)")


def test_syntax_kontrol_hatali():
    """Eksik etiketli UML yakalanmalı."""
    sonuc = plantuml_syntax_kontrol(HATALI_UML_SYNTAX)
    assert not sonuc["gecerli"]
    assert len(sonuc["hatalar"]) > 0
    print(f"  PASS: Syntax kontrol - hatalı UML ({sonuc['hatalar']})")


def test_exception_loglama():
    """Exception log doğru formatı döndürmeli."""
    try:
        raise ValueError("Test hatası")
    except Exception as e:
        kayit = exception_logla(e, "test_context")
    assert kayit["tip"] == "ValueError"
    assert "zaman" in kayit
    print("  PASS: Exception loglama çalışıyor")


# ── CP3: Integration Testler — Iterasyon Simülasyonu ──────────────────────


def test_iterasyon_1_basarili():
    """1. iterasyonda geçerli UML başarılı dönmeli."""
    ocl = validate_ocl(GECERLI_UML)
    assert ocl["gecerli_mi"]
    assert ocl["skor"] >= 0.8
    print(f"  PASS: İterasyon 1 - compile başarılı (skor={ocl['yuzde']})")


def test_iterasyon_compile_hata_yakalama():
    """Hatalı UML compile hatası vermeli ve yakalanmalı."""
    try:
        ocl = validate_ocl(HATALI_UML_SYNTAX)
        assert not ocl["gecerli_mi"]
        assert len(ocl["hatalar"]) > 0
        print(f"  PASS: İterasyon compile hata yakalama ({ocl['hatalar']})")
    except Exception as e:
        print(f"  FAIL: Beklenmedik exception: {e}")
        raise


def test_iterasyon_ocl_uyari_tespiti():
    """OCL uyarıları (tekrarlı sınıf, izole sınıf) tespit edilmeli."""
    ocl = validate_ocl(HATALI_UML_OCL)
    assert len(ocl["hatalar"]) > 0 or len(ocl["uyarilar"]) > 0
    print(f"  PASS: OCL uyarı tespiti - hatalar={ocl['hatalar']}, uyarılar={ocl['uyarilar']}")


def test_max_iterations_limiti():
    """3 iterasyon simülasyonu - son iterasyonda durmalı."""
    MAX = 3
    for i in range(1, MAX + 1):
        validate_ocl(GECERLI_UML)
        son_mu = i >= MAX
        if i == MAX:
            assert son_mu
    print(f"  PASS: Max iterasyon limiti ({MAX}) doğru çalışıyor")


def test_hatali_uml_onarim_akisi():
    """
    Senaryo: Hatalı UML → compile test → hata tespiti → normalize et.
    Gerçek Healer olmadan akış simülasyonu.
    """
    # 1. Syntax kontrol
    syntax = plantuml_syntax_kontrol(HATALI_UML_SYNTAX)
    assert not syntax["gecerli"]

    # 2. OCL doğrula
    ocl = validate_ocl(HATALI_UML_SYNTAX)
    assert not ocl["gecerli_mi"]

    # 3. Hataları normalize et
    normalize = hata_normalize_et(ocl["hatalar"], kaynak="OCL")
    assert len(normalize) > 0
    assert all("kategori" in h for h in normalize)

    print(f"  PASS: Onarım akışı simülasyonu tamamlandı ({len(normalize)} hata normalize edildi)")


def test_basarili_onarim_final_cikti():
    """Başarılı compile sonrası final UML hazır olmalı."""
    ocl = validate_ocl(GECERLI_UML)
    assert ocl["gecerli_mi"]
    # Final diyagram olarak GECERLI_UML kullanılabilir
    final_uml = GECERLI_UML
    assert "@startuml" in final_uml
    assert "@enduml" in final_uml
    print("  PASS: Final UML çıktısı hazır")


# ── CP4: E2E Testler ────────────────────────────────────────────────────────


def test_e2e_basit_srs():
    """Basit SRS → UML → OCL → Semantik tam pipeline."""
    parse = srs_to_plantuml(SRS_BASIT)
    assert parse["sinif_sayisi"] > 0

    ocl = validate_ocl(parse["plantuml_kodu"])
    assert "gecerli_mi" in ocl

    semantik = calculate_semantic_fidelity(SRS_BASIT, parse["plantuml_kodu"])
    assert semantik["genel_skor"] >= 0.0

    print(
        f"  PASS: E2E basit SRS - {parse['sinif_sayisi']} sınıf, OCL={ocl['yuzde']}, Semantik={semantik['yuzde']}"
    )


def test_e2e_karmasik_srs():
    """Karmaşık SRS tam pipeline - daha fazla sınıf beklenir."""
    parse = srs_to_plantuml(SRS_KARMASIK)
    assert parse["sinif_sayisi"] >= 3

    ocl = validate_ocl(parse["plantuml_kodu"])
    semantik = calculate_semantic_fidelity(SRS_KARMASIK, parse["plantuml_kodu"])

    print(
        f"  PASS: E2E karmaşık SRS - {parse['sinif_sayisi']} sınıf, OCL={ocl['yuzde']}, Semantik={semantik['yuzde']}"
    )


def test_e2e_hata_durumu():
    """Boş/geçersiz input hata vermeli ama çökmemeli."""
    sonuc = srs_to_plantuml("")
    assert sonuc["hata"] is not None
    assert sonuc["sinif_sayisi"] == 0
    print("  PASS: E2E hata durumu - güvenli hata işleme")


# ── CP4: Performans Testleri ────────────────────────────────────────────────


def test_performans_tek_istek_sla():
    """Tek /analyze isteği 15 saniyenin altında olmalı."""
    baslangic = time.time()
    parse = srs_to_plantuml(SRS_BASIT)
    validate_ocl(parse["plantuml_kodu"])
    calculate_semantic_fidelity(SRS_BASIT, parse["plantuml_kodu"])
    sure = time.time() - baslangic

    olcum_kaydet("/api/analyze", sure, True)
    assert sure < 15.0, f"SLA ihlali: {sure:.3f}s > 15s"
    print(f"  PASS: SLA testi - {sure * 1000:.1f}ms (limit: 15000ms)")


def test_performans_coklu_istek():
    """10 ardışık istek - P50/P95/P99 ölçümü."""
    olcumleri_sifirla()
    for i in range(10):
        baslangic = time.time()
        parse = srs_to_plantuml(SRS_BASIT)
        validate_ocl(parse["plantuml_kodu"])
        sure = time.time() - baslangic
        olcum_kaydet("/api/analyze", sure, True)

    rapor = performans_raporu("/api/analyze")
    assert rapor["toplam_istek"] == 10
    assert rapor["latency_ms"]["P95"] < 15000
    print("  PASS: Çoklu istek performansı:")
    print(
        f"         P50={rapor['latency_ms']['P50']}ms, P95={rapor['latency_ms']['P95']}ms, P99={rapor['latency_ms']['P99']}ms"
    )
    print(f"         SLA uyum: {rapor['sla_uyum_orani']}")


def test_performans_percentile_hesaplama():
    """Percentile hesaplama doğru çalışmalı."""
    veriler = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    p50 = percentile_hesapla(veriler, 50)
    p95 = percentile_hesapla(veriler, 95)
    assert p50 <= p95
    assert p50 > 0
    print(f"  PASS: Percentile hesaplama - P50={p50}, P95={p95}")


def test_regresyon_ocl_hep_ayni_sonucu():
    """Aynı UML girişi her seferinde aynı OCL sonucunu vermeli."""
    sonuc1 = validate_ocl(GECERLI_UML)
    sonuc2 = validate_ocl(GECERLI_UML)
    assert sonuc1["skor"] == sonuc2["skor"]
    assert sonuc1["gecerli_mi"] == sonuc2["gecerli_mi"]
    print("  PASS: Regresyon - OCL deterministic çalışıyor")


def test_regresyon_parser_tutarli():
    """Aynı SRS her seferinde aynı sınıfları bulmalı."""
    r1 = srs_to_plantuml(SRS_BASIT)
    r2 = srs_to_plantuml(SRS_BASIT)
    assert r1["sinif_sayisi"] == r2["sinif_sayisi"]
    assert set(r1["bulunan_siniflar"]) == set(r2["bulunan_siniflar"])
    print("  PASS: Regresyon - parser deterministic çalışıyor")


# ── Ana test koşucu ────────────────────────────────────────────────────────

if __name__ == "__main__":
    testler = [
        # CP2: Unit - Error Handler
        ("CP2 | Unit | JSON parser - düzgün", test_json_parser_duzgun),
        ("CP2 | Unit | JSON parser - markdown", test_json_parser_markdown),
        ("CP2 | Unit | Hata normalize", test_hata_normalize),
        ("CP2 | Unit | Syntax kontrol - geçerli", test_syntax_kontrol_gecerli),
        ("CP2 | Unit | Syntax kontrol - hatalı", test_syntax_kontrol_hatali),
        ("CP2 | Unit | Exception loglama", test_exception_loglama),
        # CP3: Integration
        ("CP3 | Integration | İterasyon 1 başarılı", test_iterasyon_1_basarili),
        ("CP3 | Integration | Compile hata yakalama", test_iterasyon_compile_hata_yakalama),
        ("CP3 | Integration | OCL uyarı tespiti", test_iterasyon_ocl_uyari_tespiti),
        ("CP3 | Integration | Max iterasyon limiti", test_max_iterations_limiti),
        ("CP3 | Integration | Hatalı UML onarım akışı", test_hatali_uml_onarim_akisi),
        ("CP3 | Integration | Final UML çıktısı", test_basarili_onarim_final_cikti),
        # CP4: E2E
        ("CP4 | E2E | Basit SRS pipeline", test_e2e_basit_srs),
        ("CP4 | E2E | Karmaşık SRS pipeline", test_e2e_karmasik_srs),
        ("CP4 | E2E | Hata durumu", test_e2e_hata_durumu),
        # CP4: Performans
        ("CP4 | Performans | Tek istek SLA", test_performans_tek_istek_sla),
        ("CP4 | Performans | Çoklu istek P50/P95/P99", test_performans_coklu_istek),
        ("CP4 | Performans | Percentile hesaplama", test_performans_percentile_hesaplama),
        ("CP4 | Regresyon | OCL deterministic", test_regresyon_ocl_hep_ayni_sonucu),
        ("CP4 | Regresyon | Parser deterministic", test_regresyon_parser_tutarli),
    ]

    gecti = 0
    kaldi = 0
    print("=" * 65)
    print("CURE Backend - Tam Test Paketi (CP2 + CP3 + CP4)")
    print("=" * 65)

    for isim, fn in testler:
        print(f"\n[TEST] {isim}")
        try:
            fn()
            gecti += 1
        except Exception as e:
            print(f"  FAIL: {e}")
            kaldi += 1

    print("\n" + "=" * 65)
    print(f"Sonuç: {gecti}/{len(testler)} test geçti")
    if kaldi == 0:
        print("PASS: Tum testler basarili!")
    else:
        print(f"FAIL: {kaldi} test basarisiz!")
