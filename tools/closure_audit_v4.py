"""Independent read-only v4 evidence checks. Writes only a new closure directory.

No project parser, metric or analysis function is imported here. The small
independent class/edge reader is for these stored fixtures, not general UML.
"""

from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import numpy as np
from scipy.stats import wilcoxon

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/closure_audit"
MAIN = ROOT / "backend/evaluation/results_v4/test-frozen-20261022"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(name):
    tokens = re.findall(
        r"[a-z0-9]+",
        re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", name)).lower(),
    )
    if not tokens:
        return ""
    end = tokens[-1]
    if end not in {"status", "news", "series"}:
        if end.endswith("ies") and len(end) > 4:
            end = end[:-3] + "y"
        elif end.endswith("sses"):
            end = end[:-2]
        elif len(end) > 3 and end.endswith("s") and not end.endswith(("ss", "us", "is")):
            end = end[:-1]
    return "".join(tokens[:-1] + [end])


def elements(code):
    code = re.sub(r"/\'.*?\'/", "", code, flags=re.S)
    classes, edges = set(), set()
    name = r'(?:"[^"\n]+"|[A-Za-z_][\w.]*)'
    decl = re.compile(
        r"^\s*(?:abstract\s+class|class|interface|enum)\s+(" + name + r")(?:\s+as\s+(" + name + r"))?"
    )
    edge = re.compile(
        r"^\s*("
        + name
        + r')\s*(?:"[^"\n]*"\s*)?(<\|--|--\|>|<\|\.\.|\.\.\|>|\*--|--\*|o--|--o|-->|<--|->|<-|\.\.>|<\.\.|--|\.\.)\s*(?:"[^"\n]*"\s*)?('
        + name
        + r")(?:\s*:\s*.*)?\s*$"
    )
    for line in code.splitlines():
        line = line.split("'", 1)[0]
        match = decl.match(line)
        if match:
            classes.add(norm((match[2] or match[1]).strip('"')))
        line = re.sub(r"(?<=[.\-])\[[^\]\n]+\]", "", line)
        match = edge.match(line)
        if match:
            source, op, target = match.groups()
            kind = (
                "realization"
                if "|" in op and "." in op
                else "inheritance"
                if "|" in op
                else "composition"
                if "*" in op
                else "aggregation"
                if "o" in op
                else "dependency"
                if "." in op
                else "association"
            )
            source, target = norm(source.strip('"')), norm(target.strip('"'))
            if op.startswith("<") or op.endswith(("*", "o")):
                source, target = target, source
            edges.add((source, target, kind))
    return classes, edges


def f1(a, b):
    return 2 * len(a & b) / (len(a) + len(b)) if a or b else 1.0


def desc(values):
    values = [v for v in values if v is not None]
    return {
        "n": len(values),
        "mean": statistics.mean(values) if values else None,
        "sd": statistics.stdev(values) if len(values) > 1 else 0.0 if values else None,
        "median": statistics.median(values) if values else None,
        "min": min(values) if values else None,
        "max": max(values) if values else None,
    }


def close(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, abs_tol=2e-12, rel_tol=2e-12)
    return a == b


def adjustment(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    answer, maximum = [0.0] * len(values), 0.0
    for j, index in enumerate(order):
        maximum = max(maximum, min(1.0, values[index] * (len(values) - j)))
        answer[index] = maximum
    return answer


def paired(values, labels):
    clusters = defaultdict(list)
    for value, label in zip(values, labels):
        clusters[label].append(value)
    arrays = [np.asarray(x) for x in clusters.values()]
    means = np.array([a.mean() for a in arrays])
    rng = np.random.default_rng(1729)
    draws = rng.integers(len(arrays), size=(10000, len(arrays)))
    if len({len(a) for a in arrays}) == 1:
        boot = np.stack(arrays)[draws].reshape(10000, -1).mean(axis=1)
    else:
        boot = [np.concatenate([arrays[i] for i in selected]).mean() for selected in draws]
    return {
        "mean_delta": float(np.mean(values)),
        "clusters": len(arrays),
        "bootstrap_ci": list(np.quantile(boot, [0.025, 0.975], method="linear")),
        "wilcoxon_p": float(wilcoxon(means, zero_method="wilcox", alternative="two-sided").pvalue)
        if np.any(means)
        else 1.0,
    }


def additional_statistics(rows, numbers):
    errors = []
    for s in numbers["summaries"]:
        sample = [
            r
            for r in rows
            if (r["dataset"], r["condition"], r["rep"]) == (s["dataset"], s["condition"], s["rep"])
        ]
        latencies = [r.get("end_to_end_seconds", r["elapsed_seconds"]) for r in sample]
        expected = {
            "latency": {**desc(latencies), "p95": float(np.quantile(latencies, 0.95, method="linear"))},
            "critic_compiler_project": dict(
                Counter(
                    f"critic={r['critic_valid']}|compiler={r['compiler_valid']}|project={r['project_valid']}"
                    for r in sample
                    if r["critic_valid"] is not None
                )
            ),
            "budget_exhausted": sum(r["terminated_by"] == "budget_exhausted" for r in sample),
            "regressions": sum(r["regression"] for r in sample),
            "warnings_added": sum(r["warnings_added"] for r in sample),
            "warnings_removed": sum(r["warnings_removed"] for r in sample),
            "first_compiler_valid_iteration_counts": dict(
                Counter(str(r.get("first_compiler_valid_iteration")) for r in sample)
            ),
        }
        for key, value in expected.items():
            if not close(value, s[key]):
                errors.append([s["dataset"], s["condition"], s["rep"], key])
        for key, p in s["delta_vs_input"].items():
            selected = [r for r in sample if r["metrics"] and key in r["metrics"]]
            result = paired(
                [r["metrics"][key] for r in selected], [r.get("scenario_id", r["case_id"]) for r in selected]
            )
            if not close(result, {k: p[k] for k in result}):
                errors.append([s["dataset"], s["condition"], s["rep"], key])
        token_in = sum(r["tokens_in"] for r in sample)
        token_out = sum(r["tokens_out"] for r in sample)
        if not close(
            [token_in, token_out, (token_in * 0.15 + token_out * 0.60) / 1e6],
            [s["tokens_in"], s["tokens_out"], s["estimated_cost_usd"]],
        ):
            errors.append([s["dataset"], s["condition"], "usage"])
    for s in numbers["repetitions"]:
        sample = [r for r in rows if r["dataset"] == s["dataset"] and r["condition"] == s["condition"]]
        per_case = defaultdict(list)
        for r in sample:
            per_case[r["case_id"]].append(r)
        repeated = [v for v in per_case.values() if len(v) > 1]
        disagreement = (
            sum(len({r["compiler_valid"] for r in v}) > 1 for v in repeated) / len(repeated)
            if repeated
            else None
        )
        hash_disagreement = (
            sum(len({r["output_sha256"] for r in v}) > 1 for v in repeated) / len(repeated)
            if repeated
            else None
        )
        if not close(
            [disagreement, hash_disagreement], [s["case_disagreement_rate"], s["output_disagreement_rate"]]
        ):
            errors.append([s["dataset"], s["condition"], "disagreement"])
        summaries = [
            v
            for v in numbers["summaries"]
            if v["dataset"] == s["dataset"] and v["condition"] == s["condition"]
        ]
        if not close(desc(v["compiler_rate"] for v in summaries), s["compile_rate_across_reps"]):
            errors.append([s["dataset"], s["condition"], "rep compiler SD"])
        for field, key in [
            ("reference_class", "class_f1_across_reps"),
            ("reference_rel_typed", "typed_rel_f1_across_reps"),
        ]:
            values = [v["metrics"].get(field, {}).get("all_outputs", {}).get("mean") for v in summaries]
            if not close(desc(values), s[key]):
                errors.append([s["dataset"], s["condition"], key])
    for s in numbers["defects"]:
        sample = [
            r
            for r in rows
            if (r["dataset"], r["condition"], r["rep"]) == (s["dataset"], s["condition"], s["rep"])
            and s["defect_id"] in r["defect_ids"]
        ]
        if not close(
            [len(sample), sum(r["compiler_valid"] for r in sample), len(sample) < 10],
            [s["n"], s["compiler_pass"], s["descriptive_only"]],
        ):
            errors.append([s["dataset"], s["condition"], "defect counts"])
    return errors


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []

    def record(name, ok, detail):
        records.append({"check": name, "status": "PASS" if ok else "FAIL", "evidence": detail})

    manifest = json.loads((MAIN / "manifest.json").read_text(encoding="utf-8"))
    rows = json.loads((MAIN / "results.json").read_text(encoding="utf-8"))
    numbers = json.loads((MAIN / "paper_inputs/numbers.json").read_text(encoding="utf-8"))
    files = sorted((MAIN / "cases").glob("*.json"))
    record(
        "case files equal aggregate including all fields",
        [json.loads(p.read_text(encoding="utf-8")) for p in files] == rows,
        len(files),
    )
    semantic = json.loads(
        (ROOT / "backend/evaluation/semantic_benchmark/cases.json").read_text(encoding="utf-8")
    )
    ids = (
        {f"S{i:02}" for i in range(1, 51)}
        | {f"P{i:02}" for i in range(1, 11)}
        | {r["case_id"] for r in semantic if r["split"] == "test"}
    )
    expected = {
        (c, i, rep)
        for c in [f"C{i}" for i in range(8)]
        for i in ids
        for rep in range(1, 2 if c in {"C0", "C1", "C2"} else 6)
    }
    keys = [(r["condition"], r["case_id"], r["rep"]) for r in rows]
    record(
        "registered design no duplicates or missing tuples",
        len(keys) == len(set(keys)) == 2800 and set(keys) == expected,
        {"case_ids": len(ids), "case_runs": len(rows)},
    )
    bad_hashes = [name for name, digest in manifest["output_hashes"].items() if sha(MAIN / name) != digest]
    record(
        "every declared output hash",
        not bad_hashes,
        {"checked": len(manifest["output_hashes"]), "mismatch": bad_hashes},
    )
    record(
        "prompt file bytes match manifest",
        all(sha(ROOT / p) == h for p, h in manifest["prompt_hashes"].items()),
        len(manifest["prompt_hashes"]),
    )
    record(
        "protocol file hash",
        sha(ROOT / "docs/evaluation-protocol-v4.md") == manifest["protocol_sha256"],
        manifest["protocol_commit"],
    )
    by_id = defaultdict(list)
    for r in rows:
        by_id[r["case_id"]].append(r)
    record(
        "identical input SRS/gold across conditions/repetitions",
        all(
            len({(r["srs"], r["input_plantuml"], r["gold"]) for r in group}) == 1 for group in by_id.values()
        ),
        len(by_id),
    )
    traces = [t for r in rows for t in r["trace"]]
    record(
        "call counts and raw response presence",
        len(traces) == 7936
        and all(len(r["trace"]) == r["llm_call_count"] for r in rows)
        and all(isinstance(t.get("response_text"), str) for t in traces),
        {
            "calls": len(traces),
            "models": dict(Counter(t.get("model_name") for t in traces)),
            "request_id_present": sum(bool(t.get("request_id")) for t in traces),
        },
    )
    metric_discrepancies = []
    metric_rows = [r for r in rows if r["gold"]]
    for r in metric_rows:
        gold, prediction = elements(r["gold"]), elements(r["output_plantuml"])
        before = elements(r["input_plantuml"])
        for index, field in enumerate(["reference_class", "reference_rel_typed"]):
            expected_f1 = f1(gold[index], prediction[index])
            if not close(expected_f1, r["metrics"][field]["f1"]):
                metric_discrepancies.append(
                    {
                        "case_id": r["case_id"],
                        "condition": r["condition"],
                        "rep": r["rep"],
                        "field": field,
                        "independent": expected_f1,
                        "recorded": r["metrics"][field]["f1"],
                    }
                )
            delta_field = "delta_class_f1" if index == 0 else "delta_rel_typed_f1"
            if not close(expected_f1 - f1(gold[index], before[index]), r["metrics"][delta_field]):
                metric_discrepancies.append({"case_id": r["case_id"], "field": delta_field})
    record(
        "independent fixture parser primary F1",
        not metric_discrepancies,
        {
            "case_runs": len(metric_rows),
            "discrepancies": metric_discrepancies,
            "scope": "Class and typed-edge name-set policy; not general UML semantics",
        },
    )
    groups = defaultdict(list)
    for r in rows:
        groups[(r["dataset"], r["condition"], r["rep"])].append(r)
    aggregates, mismatches = [], []
    for s in numbers["summaries"]:
        key = (s["dataset"], s["condition"], s["rep"])
        sample = groups[key]
        successes = sum(r["compiler_valid"] is True for r in sample)
        n = len(sample)
        q = successes / n
        den = 1 + 1.96**2 / n
        center = (q + 1.96**2 / (2 * n)) / den
        half = 1.96 * math.sqrt(q * (1 - q) / n + 1.96**2 / (4 * n * n)) / den
        expected_summary = {
            "n": n,
            "compiler_pass": successes,
            "compiler_rate": q,
            "project_pass": sum(r["project_valid"] is True for r in sample),
        }
        for field, value in expected_summary.items():
            if not close(value, s[field]):
                mismatches.append([list(key), field])
        if not close([center - half, center + half], [s["wilson_95"]["lower"], s["wilson_95"]["upper"]]):
            mismatches.append([list(key), "wilson"])
        for field, subsets in s["metrics"].items():
            for subset, value in subsets.items():
                chosen = [
                    r
                    for r in sample
                    if r["metrics"] and (subset == "all_outputs" or r["compiler_valid"] is True)
                ]
                if not close(desc(r["metrics"][field]["f1"] for r in chosen), value):
                    mismatches.append([list(key), field, subset])
        aggregates.append({"dataset": key[0], "condition": key[1], "rep": key[2], **expected_summary})
    record(
        "independent aggregate rates Wilson macro mean SD median",
        not mismatches,
        {"groups": len(groups), "mismatches": mismatches},
    )
    comparisons, errors = [], []
    by_key = {(r["dataset"], r["condition"], r["rep"], r["case_id"]): r for r in rows}
    for s in numbers["mcnemar"]:
        sample = sorted(
            i
            for i in ids
            if (s["dataset"], s["a"], 1 if s["a"] in {"C0", "C1", "C2"} else s["rep"], i) in by_key
        )
        pairs = [
            (
                by_key[(s["dataset"], s["a"], 1 if s["a"] in {"C0", "C1", "C2"} else s["rep"], i)][
                    s["field"]
                ],
                by_key[(s["dataset"], s["b"], 1 if s["b"] in {"C0", "C1", "C2"} else s["rep"], i)][
                    s["field"]
                ],
            )
            for i in sample
        ]
        win, loss = sum(not a and b for a, b in pairs), sum(a and not b for a, b in pairs)
        p = (
            min(1.0, 2 * sum(math.comb(win + loss, j) for j in range(min(win, loss) + 1)) / 2 ** (win + loss))
            if win + loss
            else 1.0
        )
        if not close([win, loss, p], [s["a_fail_b_pass"], s["a_pass_b_fail"], s["p_exact_two_sided"]]):
            errors.append([s["dataset"], s["rep"], s["a"], s["b"], s["field"]])
        comparisons.append({**s, "paired_rate_difference_b_minus_a": (win - loss) / len(pairs)})
    families = defaultdict(list)
    for s in comparisons:
        families[(s["dataset"], s["rep"])].append(s)
    for family in families.values():
        if not close(adjustment([r["p_exact_two_sided"] for r in family]), [r["p_holm"] for r in family]):
            errors.append("Holm family mismatch")
    record(
        "independent exact binomial McNemar and Holm",
        not errors,
        {"comparisons": len(comparisons), "errors": errors},
    )
    paired_errors, semantic_contrasts = [], []
    for s in numbers["paired_semantic"]:
        sample = sorted(
            i
            for i in ids
            if (s["dataset"], s["a"], 1 if s["a"] in {"C0", "C1", "C2"} else s["rep"], i) in by_key
        )
        values, labels = [], []
        for i in sample:
            a = by_key[(s["dataset"], s["a"], 1 if s["a"] in {"C0", "C1", "C2"} else s["rep"], i)]
            b = by_key[(s["dataset"], s["b"], 1 if s["b"] in {"C0", "C1", "C2"} else s["rep"], i)]
            if a["metrics"] and b["metrics"]:
                values.append(b["metrics"][s["metric"]]["f1"] - a["metrics"][s["metric"]]["f1"])
                labels.append(a.get("scenario_id", i))
        result = paired(values, labels)
        if not close(result, {k: s[k] for k in result}):
            paired_errors.append([s["dataset"], s["rep"], s["a"], s["b"], s["metric"]])
        semantic_contrasts.append(
            {
                **s,
                "positive_cases": sum(v > 0 for v in values),
                "negative_cases": sum(v < 0 for v in values),
                "equal_cases": sum(v == 0 for v in values),
            }
        )
    record(
        "independent scenario grouping Wilcoxon bootstrap",
        not paired_errors,
        {
            "comparisons": len(semantic_contrasts),
            "mismatches": paired_errors,
            "draws": 10000,
            "seed": 1729,
            "tolerance": 2e-12,
        },
    )
    extra_errors = additional_statistics(rows, numbers)
    record(
        "independent latency usage exhaustion iteration repetition SD defect groups and delta tests",
        not extra_errors,
        {"mismatches": extra_errors},
    )
    supplement = defaultdict(list)
    for c in semantic_contrasts:
        supplement[(c["dataset"], c["rep"])].append(c)
    for family in supplement.values():
        for c, p in zip(family, adjustment([c["wilcoxon_p"] for c in family])):
            c["audit_only_holm_sensitivity"] = p
    audit = json.loads(
        (ROOT / "backend/evaluation/results_v4/validator-audit-final-20261022/audit.json").read_text(
            encoding="utf-8"
        )
    )
    counts = Counter(
        "TP"
        if r["project_valid"] and r["compiler_valid"]
        else "FP"
        if r["project_valid"]
        else "FN"
        if r["compiler_valid"]
        else "TN"
        for r in audit["diagrams"]
    )
    record(
        "compiler agreement matrix independent recount",
        all(counts[k] == audit["confusion"][k] for k in counts),
        dict(counts),
    )
    details = {
        "base_commit": "249d0a14cc6bd2f3c449d21b87c1daa3124a8c2a",
        "no_model_calls": True,
        "original_evidence_written": False,
        "checks": records,
        "independent_aggregates": aggregates,
        "effect_sizes_mcnemar": comparisons,
        "paired_semantic_and_exploratory_multiplicity_sensitivity": semantic_contrasts,
        "input_units": {
            "case_ids": len(by_id),
            "unique_srs": len({group[0]["srs"] for group in by_id.values()}),
            "unique_diagrams": len({group[0]["input_plantuml"] for group in by_id.values()}),
            "semantic_scenarios": len(
                {group[0]["scenario_id"] for group in by_id.values() if group[0]["dataset"] == "semantic"}
            ),
        },
        "limitations": [
            "Recomputed recorded flags are not a new live compilation of every diagram.",
            "Case-level Wilson and McNemar do not adjust for within-scenario/source dependence.",
            "Wilcoxon between-condition results are unadjusted in the immutable v4 output; the audit-only Holm column is retrospective sensitivity, not preregistered.",
            "Primary F1 independently reparsed; secondary attribute/multiplicity aggregates checked against stored per-case values, not independently validated semantics.",
            "Cluster bootstrap is over scenarios within each repetition; no pooled 2800-example inference.",
        ],
    }
    (OUT / "INDEPENDENT_STATISTICS.json").write_text(
        json.dumps(details, indent=2, allow_nan=False), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "checks": len(records),
                "failed": [r["check"] for r in records if r["status"] == "FAIL"],
                "paired_comparisons": len(semantic_contrasts),
            }
        ),
        flush=True,
    )
    if any(record["status"] == "FAIL" for record in records):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
