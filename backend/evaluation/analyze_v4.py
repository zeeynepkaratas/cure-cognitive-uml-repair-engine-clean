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
    cluster_means = np.array([cluster.mean() for cluster in clusters])
    return {
        "n": len(values),
        "clusters": len(clusters),
        "wilcoxon_unit": "scenario mean difference (individual case when the scenario is unique)",
        "mean_delta": float(values.mean()),
        "wilcoxon_p": float(wilcoxon(cluster_means, alternative="two-sided", zero_method="wilcox").pvalue)
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
        latencies = [r.get("end_to_end_seconds", r["elapsed_seconds"]) for r in items]
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
            "first_compiler_valid_iteration_counts": dict(
                sorted(Counter(str(r.get("first_compiler_valid_iteration")) for r in items).items())
            ),
            "first_compiler_valid_iteration": describe(
                r.get("first_compiler_valid_iteration") for r in items
            ),
            "latency_scope": "end_to_end_seconds when recorded; legacy v4 rows use the explicitly labelled repair-loop elapsed_seconds",
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
                if rep > 1 and a in {"C0", "C1", "C2"} and b in {"C0", "C1", "C2"}:
                    continue
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

    def extra_table(stem, entries):
        if not entries:
            entries = [{"status": "not_executed_or_not_applicable"}]
        fields = list(entries[0])
        flattened = [
            {
                key: json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else value
                for key, value in row.items()
            }
            for row in entries
        ]
        with (tables / (stem + ".csv")).open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(flattened)
        content = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
        content.extend("| " + " | ".join(str(row.get(key, "")) for key in fields) + " |" for row in flattened)
        (tables / (stem + ".md")).write_text("\n".join(content) + "\n", encoding="utf-8")

        def escape(value):
            return str(value).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")

        content = [r"\begin{tabular}{" + "l" * len(fields) + "}", " & ".join(map(escape, fields)) + r" \\"]
        content.extend(" & ".join(escape(row.get(key, "")) for key in fields) + r" \\" for row in flattened)
        (tables / (stem + ".tex")).write_text("\n".join(content + [r"\end{tabular}"]), encoding="utf-8")

    extra_table("mcnemar", numbers["mcnemar"])
    extra_table("repetitions", numbers["repetitions"])
    extra_table("defects", numbers["defects"])
    reference_rows = []
    for summary in numbers["summaries"]:
        for metric, subsets in summary["metrics"].items():
            for subset, statistics in subsets.items():
                reference_rows.append(
                    {
                        "dataset": summary["dataset"],
                        "condition": summary["condition"],
                        "rep": summary["rep"],
                        "metric": metric,
                        "subset": subset,
                        **statistics,
                    }
                )
    extra_table("reference-metrics", reference_rows)
    extra_table(
        "latency-cost-warnings",
        [
            {
                "dataset": row["dataset"],
                "condition": row["condition"],
                "rep": row["rep"],
                "latency": row["latency"],
                "tokens_in": row["tokens_in"],
                "tokens_out": row["tokens_out"],
                "estimated_cost_usd": row["estimated_cost_usd"],
                "warnings_added": row["warnings_added"],
                "warnings_removed": row["warnings_removed"],
            }
            for row in numbers["summaries"]
        ],
    )
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


def combine_runs(sources, destination):
    """Combine disjoint observed records only, retaining source manifests and hashes."""
    from backend.evaluation.run_matrix import dump, write_outputs

    manifests = [
        json.loads((directory / "manifest.json").read_text(encoding="utf-8")) for directory in sources
    ]
    for key in ["protocol_sha256", "input_sha256", "prompt_hashes", "model_critic", "model_healer", "seed"]:
        if any(m[key] != manifests[0][key] for m in manifests[1:]):
            raise ValueError("Cannot combine mismatched protocols/inputs: " + key)
    if (destination / "manifest.json").exists():
        raise ValueError("Combined destination already exists")
    all_rows = {}
    for directory in sources:
        for row in json.loads((directory / "results.json").read_text(encoding="utf-8")):
            key = (row["condition"], row["case_id"], row["rep"])
            if key in all_rows:
                raise ValueError("Duplicate condition/case/repetition across source runs")
            all_rows[key] = row
    (destination / "cases").mkdir(parents=True, exist_ok=True)
    for (condition, case_id, rep), row in sorted(all_rows.items()):
        dump(destination / "cases" / f"{condition}_{case_id}_{rep}.json", row)
    manifest = {
        **manifests[0],
        "status": "combined_observations",
        "source_runs": [
            {
                "run_id": directory.name,
                "manifest": original,
                "results_sha256": hashlib.sha256((directory / "results.json").read_bytes()).hexdigest(),
            }
            for directory, original in zip(sources, manifests)
        ],
    }
    write_outputs(destination, manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--combine", nargs="+", type=Path)
    args = parser.parse_args()
    if args.combine:
        combine_runs(args.combine, args.run_dir)
    raw = args.run_dir / "results.json"
    numbers = compute(json.loads(raw.read_text(encoding="utf-8")))
    numbers["source_results_sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    output = args.run_dir / "paper_inputs"
    output.mkdir(exist_ok=True)
    (output / "numbers.json").write_text(json.dumps(numbers, indent=2, allow_nan=False), encoding="utf-8")
    render(output, numbers)
    manifest_path = args.run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["output_hashes"] = {
        str(path.relative_to(args.run_dir)).replace(chr(92), "/"): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in args.run_dir.rglob("*")
        if path.is_file() and path.name != "manifest.json" and path.suffix != ".tmp"
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
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
