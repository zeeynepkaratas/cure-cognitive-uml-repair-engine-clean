"""Read-only ZIP privacy scan, independent of Git and the export script."""

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
from zipfile import ZipFile


def scan(path, identities=()):
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None
    findings = []
    types = Counter()
    pdf_count, pdf_errors, docx_count = 0, [], 0
    patterns = {
        "absolute_user_path": r"[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_-]+|/home/[A-Za-z0-9_-]+/",
        "email_candidate": r"(?<![A-Za-z0-9_.+\-])[A-Za-z0-9_.+\-]{1,64}@[A-Za-z0-9.\-]{1,253}\.[A-Za-z]{2,24}",
        "personal_github_candidate": r"https?://github\.com/[A-Za-z0-9_\-]+/",
        "commit_or_other_sha1_breadcrumb": r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])",
        "credential_pattern": r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{28,}",
    }
    with ZipFile(path) as archive:
        names = archive.namelist()
        for name in names:
            data = archive.read(name)
            types[Path(name).suffix.lower() or "no_suffix"] += 1
            texts = [data.decode("utf-8", errors="ignore"), data.decode("utf-16-le", errors="ignore"), data.decode("utf-16-be", errors="ignore")]
            if name.lower().endswith(".pdf"):
                pdf_count += 1
                if PdfReader:
                    try:
                        pdf = PdfReader(io.BytesIO(data))
                        texts.append(str(pdf.metadata))
                        texts.extend(page.extract_text() or "" for page in pdf.pages)
                    except Exception as exc:
                        pdf_errors.append({"path": name, "error_type": type(exc).__name__})
            if name.lower().endswith(".docx"):
                docx_count += 1
                with ZipFile(io.BytesIO(data)) as nested:
                    texts.extend(nested.read(n).decode("utf-8", errors="ignore") for n in nested.namelist() if n.endswith(".xml"))
            combined = "\n".join(texts)
            categories = [label for label, pattern in patterns.items() if re.search(pattern, combined, re.I)]
            folded = combined.casefold()
            if any(token.casefold() in folded for token in identities):
                categories.append("known_contributor_identity")
            if categories:
                findings.append({"path": name, "categories": categories})
    return {
        "archive_name": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size, "members": len(names), "file_types": dict(types),
        "git_directory_present": any(n.startswith(".git/") for n in names),
        "pdf_visible_text_and_metadata": {"pdfs": pdf_count, "reader_available": PdfReader is not None, "errors": pdf_errors},
        "docx_nested_xml_scanned": docx_count, "all_member_bytes_scanned": True,
        "known_identity_tokens_checked": len(identities),
        "findings": findings, "category_file_counts": dict(Counter(c for f in findings for c in f["categories"])),
        "verdict": "CONDITIONAL: machine scan only; commit/data/source linkage and contextual human review remain OPEN",
        "limitations": ["ASCII/UTF-16 pattern and extractable PDF-text scan is not OCR or a proof of anonymity.", "Third-party dataset citations/authors may be legitimate and must not be indiscriminately removed.", "This script deliberately reports locations/categories without echoing identities or potential credentials.", "Historical Git ancestry is UNVERIFIABLE_FROM_ZIP; inspect genuine checkout separately.", "No anonymous hosting was created."],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--identities-file", type=Path, help="Private JSON token list; identities are never echoed")
    args = parser.parse_args()
    identities = json.loads(args.identities_file.read_text(encoding="utf-8")) if args.identities_file else []
    result = scan(args.archive, identities)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["archive_name", "members", "category_file_counts", "pdf_visible_text_and_metadata"]}))
