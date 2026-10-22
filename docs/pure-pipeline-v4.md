# PURE pipeline v4 execution

The official v1 XML subset was downloaded from DOI 10.5281/zenodo.1414117. Archive SHA-256: `8b0a36ac34f806d16c0c13d4b28a92b10e3fb353739025b068249b2de95fbbdb`; published MD5 verified. The ZIP contains 18 usable XML documents (the current Zenodo description says 19; no missing file was invented). The new Punkt/XML pipeline produces 7,017 rows, compared with 7,219 retained rows. The historical 34,268-to-7,219 reduction remains unreproduced: the published larger count refers to the whole collection, not this XML subset.

`pure_manifest.csv` maps every source document to its output rows. The retained CSV is unchanged. Pilot P01–P10 all align to `XMLZIPFile/0000 - cctns.xml`; exact or paraphrased wording and verified new row indices are recorded separately from the unreliable historical indices. P02 omits an opt-in condition in the source and must not be called verbatim.

The index builder implements 500-character windows with 50-character overlap, local bge-small-en-v1.5 embeddings, 384 dimensions and persisted FAISS. The CPU build has completed:7162 segments, verified dimension384 and normalized-vector self-similarity. data_pipeline/vector_db/pure_v4/ and execution_status.json record the source/output hashes and immutable model revision5c38ec7c405ec4b44b94cc5a9bb96e735b38267a. requirements-index.lock.txt records the isolated environment. Model weights were cached outside the repository. This new document index is not the rule retriever used in C0–C7; no historical index or matching retrieval performance is claimed.

Reproduce from the repository root:

```sh
python -m data_pipeline.preprocessing.download_pure --output /tmp/pure/requirements-xml.zip
python -m data_pipeline.preprocessing.xml_to_csv /tmp/pure/requirements-xml.zip
# Install requirements-index.lock.txt in a separate environment.
python -m data_pipeline.vector_db.build_index data_pipeline/datasets/pure_dataset_v2.csv --output /tmp/pure-index --model-revision 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a --batch-size 8 --threads 2
```
