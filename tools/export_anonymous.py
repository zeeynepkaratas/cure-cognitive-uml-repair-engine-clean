"""Export tracked research files without Git history, credentials or internal notes."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = ("docs/archive_internal/", ".github/")


def export(output: Path):
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    authors = set(
        subprocess.check_output(["git", "log", "--all", "--format=%an%n%ae"], cwd=ROOT).decode().splitlines()
    )
    remotes = subprocess.check_output(["git", "remote", "-v"], cwd=ROOT).decode()
    owners = set(re.findall(r"github\.com[:/]([^/\s]+)", remotes))
    identities = [
        s for s in authors | owners if s and "[bot]" not in s and not s.lower().startswith("anonymous")
    ]
    patterns = [re.compile(re.escape(s), re.I) for s in identities]
    paths = []
    leaks = []
    for name in tracked:
        if (
            not name
            or name.startswith(EXCLUDED)
            or name.endswith("_not_run.md")
            or name.startswith((".git/", ".env"))
        ):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        data = path.read_bytes()
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = ""
        if any(p.search(text) for p in patterns):
            leaks.append(name)
        if re.search(r"[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_-]+", text, re.I):
            leaks.append(name)
        paths.append((name, data))
    if leaks:
        raise ValueError("Contributor identity/path scan failed in: " + ", ".join(sorted(set(leaks))))
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as bundle:
        for name, data in paths:
            bundle.writestr(name, data)
    report = {
        "status": "passed",
        "tracked_files_exported": len(paths),
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "excluded": [
            "Git history",
            "credentials",
            "internal process notes",
            "superseded not_run notices",
            "CI workflow metadata",
        ],
        "limitation": "Content scan only. Public hosting, publication wording, retained commit hashes and datasets can still enable linkage. Upload to an independent anonymous service and review contextual clues before blind submission.",
    }
    output.with_suffix(".verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(export(args.output)))
