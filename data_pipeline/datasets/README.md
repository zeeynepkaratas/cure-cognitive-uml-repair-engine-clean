# PURE source and attribution

The citation target is PURE **v1.0**, DOI **10.5281/zenodo.1414117**.
Its DOI registration declares **Creative Commons Attribution 4.0 International
(CC BY 4.0)**. The current record is **v2.0**, DOI **10.5281/zenodo.7118517**,
with the same registered licence. Fresh DataCite rights metadata for both
DOIs was checked on 2026-10-21; direct Zenodo API requests returned HTTP 403.
The Zenodo HTML pages show the versions but their extracted licence field
contains no value. The licence declaration is therefore corroborated using
the official DOI registry, not inferred from a blank HTML field.

The v2.0 description says the curators do not know of licence agreements or
intellectual property rights in the collected requirements, and offers removal
on infringement reports. This caveat remains relevant even though the
registration declares CC BY 4.0. Citing v1.0 does not establish which archive
version CURE actually consumed: **NOT RECORDED**.

Sources:

- Record: https://zenodo.org/records/1414117
- License: https://creativecommons.org/licenses/by/4.0/
- Dataset DOI: https://doi.org/10.5281/zenodo.1414117
- Requested publication citation: Alessio Ferrari, Giorgio Oronzo Spagnolo,
  and Stefania Gnesi. 2017. PURE: A Dataset of Public Requirements Documents.
  IEEE International Requirements Engineering Conference, pp. 502–505.
  https://doi.org/10.1109/RE.2017.29

Reuse must credit the source, link to the license, and indicate changes. The
CURE MIT license does not replace this license or third-party document rights.
The upstream record's license declaration is recorded here; this is not an
independent determination of rights in every original requirements document.

## Historical data and new reconstruction

The original pure_dataset.csv has7219 rows and is retained unchanged. Its historical consumed archive version and exact34268-to7219 filtering procedure are NOT RECORDED. The new pipeline does not claim to reproduce that historical procedure. The original publication's79 documents and34268 sentences describe a larger collection than the downloaded XML subset.

The v4 reconstruction independently downloads requirements-xml.zip from official v1.0. pure_archive_manifest.json records SHA-2568b0a36ac34f806d16c0c13d4b28a92b10e3fb353739025b068249b2de95fbbdb,378737 bytes and the matching published MD5. This archive contains18 usable XML documents; the current record description says19. The missing nineteenth file was not invented.

The XML/HTML/Punkt pipeline produces pure_dataset_v2.csv with7017 rows, preserving source document and sentence metadata. pure_manifest.csv maps every source document to output rows. See pure_dataset_v2.status.json and docs/pure-pipeline-v4.md for the exact filter and reproduction commands.

P01–P10 are all aligned to XMLZIPFile/0000 - cctns.xml in the official archive. pure_pilot_provenance.csv retains historical row indices and CSV text, adds verified new row indices and exact source sentences, and labels each pilot requirement verbatim or paraphrase. Historical indices are not treated as authoritative. P02 omits the source opt-in condition; this is a substantive paraphrase qualification. Pilot reference UML models and injected defects were authored for CURE, not supplied as PURE gold annotations.

The optional local index was actually built from the new source-linked CSV:7162 segments of at most500 characters with50-character overlap, normalized384-dimensional bge-small-en-v1.5 vectors and persisted FAISS. The exact immutable model revision, source/output hashes and separate package lock are recorded in ../vector_db/. This document index is separate from the rule retriever used in the experiment matrix.
