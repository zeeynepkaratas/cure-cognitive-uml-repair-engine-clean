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
version CURE actually consumed: **BULUNAMADI**.

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

## Changes and retained provenance

`pure_dataset.csv` contains 7,219 rows and only the `Requirement` column. The
converter in `../preprocessing/xml_to_csv.py` removes XML markup, normalizes
whitespace, splits text, drops short fragments, and removes duplicates. The
pilot further selects/paraphrases requirement excerpts, creates reference UML
models manually, and injects defects. These are CURE transformations, not
upstream PURE reference models.

The original PURE publication describes 79 documents and 34,268 sentences.
Those full-corpus counts do **not** establish how many original documents were
actually read to produce this repository's CSV. The raw source archive and a
document-to-row manifest were not retained: **BULUNAMADI**. Consequently the
exact count and original filenames of documents used for P01–P10 cannot be
verified from the retained CSV. Its opening text identifies CCTNS material,
but this alone does not prove the original document identity for each P-case.

`pure_pilot_provenance.csv` preserves the stored `pure_row` values, actual CSV
row text, and normalized exact text matches (where present). It explicitly
leaves original document names unresolved rather than guessing a row convention.
See `../../docs/submission-audit-2026-10-20/pure_license_record.json` for the
upstream license metadata retrieved on 2026-10-20. Download verification of
the original archive used by CURE: **BULUNAMADI**.
