"""Optional local bge-small-en-v1.5/FAISS index, never an embedding API."""

import argparse
import csv
import hashlib
import json
from pathlib import Path


def segments(text: str, size: int = 500, overlap: int = 50):
    if not 0 <= overlap < size:
        raise ValueError("Require 0 <= overlap < size")
    for start in range(0, len(text), size - overlap):
        yield text[start : start + size]
        if start + size >= len(text):
            break


def build(dataset: Path, destination: Path, model_revision: str, batch_size: int = 8, threads: int = 2):
    import faiss
    from sentence_transformers import SentenceTransformer
    import numpy as np
    import torch

    if batch_size < 1 or threads < 1:
        raise ValueError("Batch size and threads must be positive")
    if destination.exists():
        raise ValueError("Choose a new index destination; existing evidence is protected")
    torch.set_num_threads(threads)

    with dataset.open(encoding="utf-8-sig", newline="") as stream:
        chunks = [
            {
                "text": chunk,
                "source_document": row["source_document"],
                "row_id": row["row_id"],
                "chunk_index": i,
            }
            for row in csv.DictReader(stream)
            for i, chunk in enumerate(segments(row["Requirement"]))
        ]
    model = SentenceTransformer("BAAI/bge-small-en-v1.5", revision=model_revision, device="cpu")
    vectors = model.encode(
        [c["text"] for c in chunks], normalize_embeddings=True, batch_size=batch_size, show_progress_bar=False
    ).astype(np.float32)
    if vectors.shape[1] != 384:
        raise ValueError("Expected 384-dimensional bge embeddings")
    index = faiss.IndexFlatIP(384)
    index.add(vectors)
    destination.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(destination / "index.faiss"))
    (destination / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    record = {
        "status": "executed",
        "model": "BAAI/bge-small-en-v1.5",
        "model_revision": model_revision,
        "dimension": 384,
        "segment_chars": 500,
        "overlap_chars": 50,
        "chunk_count": len(chunks),
        "batch_size": batch_size,
        "cpu_threads": threads,
        "dataset_sha256": hashlib.sha256(dataset.read_bytes()).hexdigest(),
    }
    record["output_sha256"] = {
        name: hashlib.sha256((destination / name).read_bytes()).hexdigest()
        for name in ["index.faiss", "chunks.json"]
    }
    (destination / "manifest.json").write_text(json.dumps(record, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-revision", required=True, help="Immutable Hugging Face model revision")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--threads", type=int, default=2)
    args = parser.parse_args()
    build(args.dataset, args.output, args.model_revision, args.batch_size, args.threads)
