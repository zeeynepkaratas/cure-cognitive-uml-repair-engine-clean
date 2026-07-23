"""CURE deney ve hata loglari icin kucuk analiz araci.

Kullanim:
    python ai_core/log_analiz.py results/autonomous_repair_results.json
    python ai_core/log_analiz.py results/autonomous_repair_results.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean


def _load_records(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Log dosyasi bulunamadi: {path}")

    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data.get("results", data.get("loglar", []))
        return data

    if path.suffix.lower() == ".csv":
        with path.open("r", newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    raise ValueError("Sadece .json veya .csv log dosyalari desteklenir.")


def summarize(records: list[dict]) -> dict:
    total = len(records)
    if total == 0:
        return {"total": 0, "success_rate": 0.0, "average_duration": 0.0}

    success_values = [
        str(item.get("basarili", item.get("success", ""))).lower() in {"true", "1", "yes"}
        for item in records
    ]
    durations = []
    for item in records:
        value = item.get("sure_saniye", item.get("duration_seconds"))
        try:
            durations.append(float(value))
        except (TypeError, ValueError):
            continue

    return {
        "total": total,
        "successful": sum(success_values),
        "failed": total - sum(success_values),
        "success_rate": round(sum(success_values) / total, 4),
        "average_duration": round(mean(durations), 4) if durations else 0.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="CURE deney loglarini ozetler.")
    parser.add_argument("path", help="CSV veya JSON log dosyasi")
    args = parser.parse_args()

    summary = summarize(_load_records(Path(args.path)))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
