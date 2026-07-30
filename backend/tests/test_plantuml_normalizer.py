import os
import sys


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AI_CORE_SRC = os.path.join(REPO_ROOT, "ai_core", "src")
sys.path.insert(0, AI_CORE_SRC)

from ai.plantuml_normalizer import normalize_plantuml_text


def test_extracts_fenced_plantuml_without_prose():
    raw = """Here is the repaired diagram:

```plantuml
@startuml
class UserManager {}
@enduml
```

Done."""
    normalized = normalize_plantuml_text(raw)
    assert normalized == "@startuml\nclass UserManager {}\n@enduml"


def test_trims_unfenced_prose_around_plantuml_boundaries():
    raw = "Fixed version:\n@startuml\nclass ReportService {}\n@enduml\nThis should compile."
    normalized = normalize_plantuml_text(raw)
    assert normalized == "@startuml\nclass ReportService {}\n@enduml"


def test_keeps_missing_boundary_output_for_validator_to_catch():
    raw = "class UserManager {}\n@enduml\nAdditional note"
    normalized = normalize_plantuml_text(raw)
    assert normalized == "class UserManager {}\n@enduml"
    assert not normalized.startswith("@startuml")


if __name__ == "__main__":
    tests = [
        test_extracts_fenced_plantuml_without_prose,
        test_trims_unfenced_prose_around_plantuml_boundaries,
        test_keeps_missing_boundary_output_for_validator_to_catch,
    ]
    passed = 0
    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")
    print(f"Sonuc: {passed}/{len(tests)} test gecti")
