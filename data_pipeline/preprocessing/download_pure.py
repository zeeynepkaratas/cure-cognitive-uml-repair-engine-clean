"""Download the official PURE v1 XML subset and verify the published checksum."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://zenodo.org/records/1414117/files/requirements-xml.zip?download=1"
MD5 = "c81235c40f88a2c947ae66e0eddad585"


def download(output: Path):
    with urlopen(Request(URL, headers={"User-Agent": "CURE-reproducibility/4.0"}), timeout=45) as response:
        data = response.read()
    if hashlib.md5(data).hexdigest() != MD5:
        raise ValueError("PURE archive differs from Zenodo published MD5")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    record = {
        "doi": "10.5281/zenodo.1414117",
        "version": "1.0",
        "url": URL,
        "archive": output.name,
        "md5": MD5,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }
    output.with_suffix(".manifest.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(download(args.output)))
