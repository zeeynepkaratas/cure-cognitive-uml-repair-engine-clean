# Local PURE document index

The reproducible CPU build uses the source-linked PURE v2 CSV, 500-character segments with 50-character overlap, BAAI/bge-small-en-v1.5 at immutable revision5c38ec7c405ec4b44b94cc5a9bb96e735b38267a, normalized384-dimensional embeddings and a persisted FAISS IndexFlatIP.

The executed artifact in pure_v4/ contains7162 chunks, index.faiss, chunks.json and manifest.json. execution_status.json records the source and output hashes. Model weights are cached outside the artifact. Install requirements-index.lock.txt in a separate environment; no embedding API is used.

```sh
python data_pipeline/vector_db/build_index.py data_pipeline/datasets/pure_dataset_v2.csv --output /tmp/pure-index-new --model-revision 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a --batch-size 8 --threads 2
```

Choose a fresh destination: the builder refuses to overwrite an existing index. This document index is separate from the disclosed local rule catalogue retrieved in C5/C7. The experiment matrix does not silently substitute document retrieval for rule retrieval. It also does not reproduce the historical OpenAI-embedding ranking.
