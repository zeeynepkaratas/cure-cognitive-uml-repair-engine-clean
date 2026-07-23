"""Run reproducible autonomous-repair experiments and write CSV/JSON logs.

The script imports the FastAPI endpoint directly, so it does not require a
running server. If the AI agent cannot run, the endpoint records its deterministic
fallback path and the experiment remains reproducible.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from src.api.endpoints import AutonomousRepairRequest, autonomous_repair  # noqa: E402


SCENARIOS = [
    {
        "id": "missing-start-end",
        "srs_metni": "The UserManager handles authentication.",
        "plantuml_kodu": "class UserManager {}",
    },
    {
        "id": "missing-end",
        "srs_metni": "The DiagramService generates diagrams.",
        "plantuml_kodu": "@startuml\nclass DiagramService {}",
    },
    {
        "id": "valid-single-class",
        "srs_metni": "The ReportService creates reports.",
        "plantuml_kodu": "@startuml\nclass ReportService {}\n@enduml",
    },
    {
        "id": "lowercase-class",
        "srs_metni": "The UserManager handles users.",
        "plantuml_kodu": "@startuml\nclass userManager {}\n@enduml",
    },
]


def run(max_iterations: int) -> list[dict]:
    rows = []
    for scenario in SCENARIOS:
        response = autonomous_repair(
            AutonomousRepairRequest(
                plantuml_kodu=scenario["plantuml_kodu"],
                srs_metni=scenario["srs_metni"],
                max_iterations=max_iterations,
            )
        )
        rows.append(
            {
                "scenario_id": scenario["id"],
                "basarili": response["basarili"],
                "sure_saniye": response["sure_saniye"],
                "max_iterations": response["max_iterations"],
                "iteration_count": len(response["iterasyonlar"]),
                "final_status": response["iterasyonlar"][-1]["status"],
                "final_plantuml": response["final_plantuml"],
            }
        )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "autonomous_repair_results.csv"
    json_path = output_dir / "autonomous_repair_results.json"

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scenario_count": len(rows),
        "success_count": sum(1 for row in rows if row["basarili"]),
        "success_rate": round(sum(1 for row in rows if row["basarili"]) / len(rows), 4),
        "results": rows,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return csv_path, json_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CURE autonomous repair experiments.")
    parser.add_argument("--max-iterations", type=int, default=3, choices=[1, 2, 3, 4, 5])
    parser.add_argument("--output-dir", default=str(ROOT / "results"))
    args = parser.parse_args()

    rows = run(args.max_iterations)
    csv_path, json_path = write_outputs(rows, Path(args.output_dir))
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
