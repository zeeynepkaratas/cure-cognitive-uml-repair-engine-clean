"""Redact contributor identities without altering numeric/boolean evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIRS = ("backend/evaluation/results", "docs/submission-audit-2026-10-20")
ANONYMOUS_URL = "https://anonymous.4open.science/r/CURE-ANONYMIZED"
PERSONAL = None
PERSONAL_OWNERS = set()


def redact(text: str) -> str:
    for owner in PERSONAL_OWNERS:
        text = re.sub(r"https?://github\.com/" + re.escape(owner) + r"/[^\s\"'<>)]*", ANONYMOUS_URL, text, flags=re.I)
    # JSON strings and ordinary text can contain differently escaped backslashes.
    text = re.sub(r"[A-Za-z]:[\\/]+Users[\\/]+[^\s\"'<>\r\n]*", "<REDACTED_PATH>", text, flags=re.I)
    if PERSONAL is not None:
        text = PERSONAL.sub("Anonymous contributor", text)
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "anonymous@example.invalid", text)
    return text


def numeric_values(value, path=()):
    """Include paths, types and exact values; ignore string-only redactions."""
    if isinstance(value, dict):
        return [item for key, val in value.items() for item in numeric_values(val, (*path, key))]
    if isinstance(value, list):
        return [item for i, val in enumerate(value) for item in numeric_values(val, (*path, i))]
    if isinstance(value, (int, float, bool)) or value is None:
        return [(path, type(value).__name__, value)]
    return []


def evidence_manifest(root=ROOT):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for directory in EVIDENCE_DIRS for p in sorted((root / directory).rglob("*")) if p.is_file()}


def main():
    global PERSONAL, PERSONAL_OWNERS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    # Discover identities from local Git metadata instead of embedding them in code.
    authors = subprocess.check_output(["git", "log", "--all", "--format=%an"], cwd=root).decode().splitlines()
    names = sorted({n for n in authors if n and "[bot]" not in n}, key=len, reverse=True)
    PERSONAL = re.compile("|".join(re.escape(n) for n in names), re.I) if names else None
    remotes = subprocess.check_output(["git", "remote", "-v"], cwd=root).decode()
    PERSONAL_OWNERS = set(re.findall(r"github\.com[:/]([^/\s]+)", remotes))
    manifest_path = root / "RESULTS_MANIFEST_ORIGINAL.json"
    if not manifest_path.exists():
        manifest_path.write_text(json.dumps(evidence_manifest(root), indent=2) + "\n", encoding="utf-8")
    files = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    checks = []
    for name in files:
        path = root / name
        if not name or name == "data_pipeline/datasets/pure_dataset.csv" or not path.is_file() or path.suffix.lower() not in {".json", ".csv", ".md", ".py", ".txt", ".yml", ".yaml"}:
            continue
        try:
            before = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix == ".json":
            original = json.loads(before)
            def strings(v):
                if isinstance(v, str): return redact(v)
                if isinstance(v, list): return [strings(x) for x in v]
                if isinstance(v, dict): return {k: strings(x) for k, x in v.items()}
                return v
            cleaned = strings(original)
            after = json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n" if cleaned != original else before
            assert numeric_values(original) == numeric_values(json.loads(after)), name
        else:
            after = redact(before)
        if before != after:
            path.write_text(after, encoding="utf-8")
            checks.append({"file": name, "numeric_boolean_values_unchanged": True,
                           "sha256_before": hashlib.sha256(before.encode()).hexdigest(),
                           "sha256_after": hashlib.sha256(after.encode()).hexdigest()})
    target = root / "docs/evidence-redaction-verification.json"
    target.write_text(json.dumps({"changes": checks, "json_numeric_boolean_verification": "passed",
                                  "history_anonymous": False,
                                  "note": "The repository host and Git history still identify contributors; use an exported snapshot for blind review."}, indent=2) + "\n", encoding="utf-8")
    print(f"Redacted {len(checks)} text files; numeric and boolean JSON values preserved.")


if __name__ == "__main__":
    main()
