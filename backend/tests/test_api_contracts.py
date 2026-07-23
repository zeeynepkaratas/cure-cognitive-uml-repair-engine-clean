import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.api.endpoints import (
        AutonomousRepairRequest,
        PerformansOlcumGirdisi,
        SRSGirdisi,
        UMLDogrulamaGirdisi,
        generate_uml,
        autonomous_repair,
        performans_getir,
        performans_olcum_kaydet,
        plantuml_render_et,
    )
except ModuleNotFoundError as exc:
    if exc.name == "fastapi":
        print("SKIP: fastapi paketi bu ortamda kurulu degil; requirements.txt ile kurulunca API kontrat testi calisir.")
        sys.exit(0)
    raise


SRS = """
The UserManager handles user authentication.
The DiagramService generates PlantUML diagrams.
The UserManager uses the DiagramService.
"""


def test_generate_uml_endpoint_contract():
    response = generate_uml(SRSGirdisi(metin=SRS))
    assert response["basarili"] is True
    assert "@startuml" in response["plantuml_kodu"]
    assert "svg" in response["render"]
    assert "png_base64" in response["render"]
    print("PASS: /generate-uml JSON + SVG/PNG contract")


def test_render_endpoint_contract():
    plantuml = "@startuml\nclass UserManager {}\n@enduml"
    response = plantuml_render_et(UMLDogrulamaGirdisi(plantuml_kodu=plantuml))
    assert response["basarili"] is True
    assert response["compile"]["basarili"] is True
    assert response["render"]["formatlar"] == ["svg", "png"]
    print("PASS: /api/render compile + render contract")


def test_autonomous_repair_final_flow():
    response = autonomous_repair(AutonomousRepairRequest(plantuml_kodu="class UserManager {}"))
    assert response["basarili"] is True
    assert response["final_plantuml"].startswith("@startuml")
    assert response["final_render"]["svg"]
    assert len(response["iterasyonlar"]) <= 3
    print("PASS: /api/autonomous-repair final diagram flow")


def test_performance_report_flow():
    performans_olcum_kaydet(
        PerformansOlcumGirdisi(endpoint="/api/analyze", sure_saniye=0.01, basarili=True)
    )
    report = performans_getir("/api/analyze")
    assert report["toplam_istek"] >= 1
    assert report["latency_ms"]["P95"] < 15000
    print("PASS: /api/performance SLA report flow")


if __name__ == "__main__":
    tests = [
        test_generate_uml_endpoint_contract,
        test_render_endpoint_contract,
        test_autonomous_repair_final_flow,
        test_performance_report_flow,
    ]
    passed = 0
    for test in tests:
        test()
        passed += 1
    print(f"Sonuc: {passed}/{len(tests)} test gecti")
