"""Analyze completed raw case records; missing LLM conditions are never imputed."""

from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from scipy.stats import binomtest, wilcoxon

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from backend.evaluation.reference_metrics import describe, macro
from backend.evaluation.repair_benchmark_utils import wilson_interval


def exact_mcnemar(a, b):
    if len(a) != len(b):
        raise ValueError("Paired lengths differ")
    win = sum(x is False and y is True for x, y in zip(a, b))
    loss = sum(x is True and y is False for x, y in zip(a, b))
    return {
        "a_fail_b_pass": win,
        "a_pass_b_fail": loss,
        "both_pass": sum(x is True and y is True for x, y in zip(a, b)),
        "both_fail": sum(x is False and y is False for x, y in zip(a, b)),
        "p_exact_two_sided": float(binomtest(win, win + loss, 0.5).pvalue) if win + loss else 1.0,
    }


def holm(values):
    ordered = sorted(enumerate(values), key=lambda pair: pair[1])
    corrected = [0.0] * len(values)
    last = 0.0
    for rank, (i, p) in enumerate(ordered):
        last = max(last, min(1.0, (len(values) - rank) * p))
        corrected[i] = last
    return corrected


def paired_delta(values, groups, seed=1729, draws=10000):
    if not values:
        return {"n": 0, "wilcoxon_p": None, "bootstrap_ci": None}
    values = np.array(values, dtype=float)
    grouped = defaultdict(list)
    for group, value in zip(groups, values):
        grouped[group].append(value)
    clusters = [np.array(v) for v in grouped.values()]
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(draws):
        sample = rng.integers(0, len(clusters), size=len(clusters))
        means.append(float(np.concatenate([clusters[i] for i in sample]).mean()))
    return {
        "n": len(values),
        "clusters": len(clusters),
        "mean_delta": float(values.mean()),
        "wilcoxon_p": float(wilcoxon(values, alternative="two-sided", zero_method="wilcox").pvalue)
        if np.any(values)
        else 1.0,
        "bootstrap_ci": list(map(float, np.quantile(means, [0.025, 0.975], method="linear"))),
        "bootstrap_draws": draws,
        "bootstrap_seed": seed,
        "all_zero": not bool(np.any(values)),
    }


def compute(rows):
    complete = [r for r in rows if r.get("run_status", "completed") == "completed"]
    summaries = []
    groups = defaultdict(list)
    for row in complete:
        groups[(row["dataset"], row["condition"], row["rep"])].append(row)
    for (dataset, condition, rep), items in sorted(groups.items()):
        valid = [r for r in items if type(r.get("compiler_valid")) is bool]
        successes = sum(r["compiler_valid"] for r in valid)
        critic = Counter(
            f"critic={r['critic_valid']}|compiler={r['compiler_valid']}|project={r['project_valid']}"
            for r in items
            if r["critic_valid"] is not None
        )
        latencies = [r["elapsed_seconds"] for r in items]
        met = [r for r in items if r.get("metrics")]
        usage_known = all(r["tokens_in"] is not None and r["tokens_out"] is not None for r in items)
        tokens_in = sum(r["tokens_in"] for r in items) if usage_known else None
        tokens_out = sum(r["tokens_out"] for r in items) if usage_known else None
        summary = {
            "dataset": dataset,
            "condition": condition,
            "rep": rep,
            "n": len(items),
            "compiler_available_n": len(valid),
            "compiler_pass": successes,
            "compiler_rate": successes / len(valid) if valid else None,
            "wilson_95": wilson_interval(successes, len(valid)) if valid else None,
            "project_pass": sum(r["project_valid"] for r in items),
            "agent_status_counts": dict(Counter(r["agent_status"] for r in items)),
            "regressions": sum(r["regression"] for r in items),
            "compiler_pass_if_reverted": sum(r["compiler_valid_if_reverted"] is True for r in items),
            "budget_exhausted": sum(r["terminated_by"] == "budget_exhausted" for r in items),
            "budget_exhaustion_rate": sum(r["terminated_by"] == "budget_exhausted" for r in items)
            / len(items),
            "critic_compiler_project": dict(sorted(critic.items())),
            "first_compiler_valid_iteration": describe(
                r.get("first_compiler_valid_iteration") for r in items
            ),
            "latency": {**describe(latencies), "p95": float(np.quantile(latencies, 0.95, method="linear"))},
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "estimated_cost_usd": (tokens_in * 0.15 + tokens_out * 0.60) / 1e6 if usage_known else None,
            "warnings_added": sum(r["warnings_added"] for r in items),
            "warnings_removed": sum(r["warnings_removed"] for r in items),
            "reference_sizes": {
                "classes": describe(r["metrics"]["reference_class_count"] for r in met),
                "relationships": describe(r["metrics"]["reference_relationship_count"] for r in met),
            },
            "metrics": {
                key: macro(met, key)
                for key in [
                    "reference_class",
                    "reference_rel_undirected",
                    "reference_rel_directed",
                    "reference_rel_typed",
                    "reference_rel_multiplicity",
                    "reference_attribute",
                ]
            }
            if met
            else {},
            "delta_vs_input": {
                key: paired_delta(
                    [r["metrics"][key] for r in met if key in r["metrics"]],
                    [r.get("scenario_id", r["case_id"]) for r in met if key in r["metrics"]],
                )
                for key in ["delta_class_f1", "delta_rel_typed_f1"]
            }
            if met
            else {},
        }
        summaries.append(summary)
    comparisons = []
    datasets = sorted({r["dataset"] for r in complete})
    for dataset in datasets:
        reps = sorted({r["rep"] for r in complete if r["dataset"] == dataset})
        conditions = sorted({r["condition"] for r in complete if r["dataset"] == dataset})
        for rep in reps:
            by = {
                c: {
                    r["case_id"]: r
                    for r in complete
                    if r["dataset"] == dataset
                    and r["condition"] == c
                    and r["rep"] == (1 if c in {"C0", "C1", "C2"} else rep)
                }
                for c in conditions
            }
            pairs = [("C0", c) for c in conditions if c != "C0"] + [
                (c, "C7") for c in ["C1", "C2", "C3", "C4", "C5"] if c in conditions and "C7" in conditions
            ]
            family = []
            for a, b in pairs:
                if not by[a] or not by[b]:
                    continue
                common = sorted(set(by[a]) & set(by[b]))
                for field in ["compiler_valid", "project_valid"]:
                    ids = [
                        i for i in common if type(by[a][i][field]) is bool and type(by[b][i][field]) is bool
                    ]
                    result = {
                        "dataset": dataset,
                        "rep": rep,
                        "a": a,
                        "b": b,
                        "field": field,
                        "paired_n": len(ids),
                        **exact_mcnemar([by[a][i][field] for i in ids], [by[b][i][field] for i in ids]),
                    }
                    family.append(result)
            for result, corrected in zip(family, holm([r["p_exact_two_sided"] for r in family])):
                result["p_holm"] = corrected
            comparisons.extend(family)
    repetitions = []
    for dataset in datasets:
        for condition in sorted({r["condition"] for r in complete if r["dataset"] == dataset}):
            sample = [s for s in summaries if s["dataset"] == dataset and s["condition"] == condition]
            by_case = defaultdict(list)
            for row in complete:
                if row["dataset"] == dataset and row["condition"] == condition:
                    by_case[row["case_id"]].append(row["compiler_valid"])
            repeated = {key: values for key, values in by_case.items() if len(values) > 1}
            repetitions.append(
                {
                    "dataset": dataset,
                    "condition": condition,
                    "repetitions_observed": len(sample),
                    "compile_rate_across_reps": describe(s["compiler_rate"] for s in sample),
                    "case_disagreement_rate": sum(len(set(v)) > 1 for v in repeated.values()) / len(repeated)
                    if repeated
                    else None,
                    "per_case_disagreement": {
                        key: len(set(values)) > 1 for key, values in sorted(repeated.items())
                    },
                }
            )
    defects = []
    for dataset, condition, rep in sorted(groups):
        by_defect = defaultdict(list)
        for row in groups[(dataset, condition, rep)]:
            for defect in row["defect_ids"]:
                by_defect[defect].append(row)
        for defect, items in sorted(by_defect.items()):
            defects.append(
                {
                    "dataset": dataset,
                    "condition": condition,
                    "rep": rep,
                    "defect_id": defect,
                    "n": len(items),
                    "descriptive_only": len(items) < 10,
                    "compiler_pass": sum(r["compiler_valid"] is True for r in items),
                    "delta_class_f1": describe(
                        r["metrics"].get("delta_class_f1") for r in items if r.get("metrics")
                    ),
                }
            )
    observed = sorted({r["condition"] for r in complete})
    return {
        "schema_version": 4,
        "completed_case_runs": len(complete),
        "incomplete_case_runs": len(rows) - len(complete),
        "observed_conditions": observed,
        "missing_conditions": [f"C{i}" for i in range(8) if f"C{i}" not in observed],
        "summaries": summaries,
        "mcnemar": comparisons,
        "repetitions": repetitions,
        "defects": defects,
        "limitations": [
            "No unobserved LLM condition is filled with retained results.",
            "Compiler agreement is not semantic validity.",
            "Semantic models share a curated template; independent expert review is pending.",
            "Latency includes cached validation requests; compare timing cautiously.",
        ],
    }


def render(directory, numbers):
    tables = directory / "tables"
    figures = directory / "figures"
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(exist_ok=True)
    rows = [
        {
            k: s[k]
            for k in [
                "dataset",
                "condition",
                "rep",
                "n",
                "compiler_pass",
                "compiler_rate",
                "project_pass",
                "regressions",
                "estimated_cost_usd",
            ]
        }
        for s in numbers["summaries"]
    ]
    columns = list(rows[0]) if rows else ["dataset", "condition"]
    with (tables / "outcomes.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    lines.extend("| " + " | ".join(str(row[c]) for c in columns) + " |" for row in rows)
    (tables / "outcomes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    tex = [
        "\\begin{tabular}{" + "l" * len(columns) + "}",
        " & ".join(c.replace("_", r"\_") for c in columns) + r" \\",
    ]
    tex.extend(" & ".join(str(row[c]).replace("_", r"\_") for c in columns) + r" \\" for row in rows)
    (tables / "outcomes.tex").write_text("\n".join(tex + ["\\end{tabular}"]), encoding="utf-8")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 4))
    labels = [f"{s['dataset']}/{s['condition']}/r{s['rep']}" for s in numbers["summaries"]]
    ax.bar(labels, [s["compiler_rate"] or 0 for s in numbers["summaries"]])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Observed compilation rate")
    ax.tick_params(axis="x", rotation=70)
    fig.tight_layout()
    fig.savefig(figures / "compile-rate.pdf")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4))
    data = [
        d
        for d in numbers["defects"]
        if d["dataset"] == "semantic" and d["delta_class_f1"]["mean"] is not None
    ]
    ax.bar([d["condition"] + "/" + d["defect_id"] for d in data], [d["delta_class_f1"]["mean"] for d in data])
    ax.set_ylabel("Mean class delta-F1 (descriptive)")
    ax.tick_params(axis="x", rotation=90)
    fig.tight_layout()
    fig.savefig(figures / "delta-f1-defect.pdf")
    plt.close(fig)
    for filename, title, field in [
        ("critic-confusion.pdf", "Critic/compiler/project observations", "critic_compiler_project"),
        ("iteration-trace.pdf", "First compiler-valid iteration", "first_compiler_valid_iteration"),
    ]:
        fig, ax = plt.subplots(figsize=(8, 4))
        observed = [s for s in numbers["summaries"] if s["condition"] not in {"C0", "C1", "C2"}]
        if not observed:
            ax.text(0.5, 0.5, "LLM conditions not executed", ha="center", va="center")
            ax.set_axis_off()
        else:
            ax.text(
                0.01,
                0.99,
                "\n".join(f"{s['dataset']}/{s['condition']}/r{s['rep']}: {s[field]}" for s in observed),
                va="top",
                fontsize=6,
                wrap=True,
            )
            ax.set_axis_off()
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(figures / filename)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    raw = args.run_dir / "results.json"
    numbers = compute(json.loads(raw.read_text(encoding="utf-8")))
    numbers["source_results_sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    output = args.run_dir / "paper_inputs"
    output.mkdir(exist_ok=True)
    (output / "numbers.json").write_text(json.dumps(numbers, indent=2, allow_nan=False), encoding="utf-8")
    render(output, numbers)
    print(
        json.dumps(
            {
                "completed_case_runs": numbers["completed_case_runs"],
                "observed_conditions": numbers["observed_conditions"],
                "missing_conditions": numbers["missing_conditions"],
            }
        )
    )


if __name__ == "__main__":
    main()
