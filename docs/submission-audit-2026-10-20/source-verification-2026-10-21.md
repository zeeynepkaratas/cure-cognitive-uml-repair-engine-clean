# Source verification for submission v3

## PURE

Citation target: v1.0, https://doi.org/10.5281/zenodo.1414117.
Current record: v2.0, https://doi.org/10.5281/zenodo.7118517.
Both official DataCite registrations report CC BY 4.0. The extracted Zenodo
HTML licence values are blank; the Zenodo API returned HTTP 403. The existing
2026-10-20 v1 API snapshot and fresh 2026-10-21 DataCite rights are preserved
in `pure_license_record.json`. The v2 description qualifies this declaration
by disclaiming knowledge of agreements or rights in the source requirements.
The archive version actually used by CURE remains BULUNAMADI.

## Related-work labels

- MPC-Coder: https://www.mdpi.com/2073-8994/18/2/248 . Section 4.3.3 describes
  extracting the graph with LLM assistance and validating it with experts.
  Section 3.3.2 describes compiler and model-checker feedback driving repair;
  Sections 3.2.2–3.2.3 describe vector retrieval alongside graph constraints.
  The existing sentence and KG+RAG / Multi-Agent / Repair=Yes labels are supported.
  The expert-review passage is in 4.3.3, not 4.3.2.
- DocSync: https://arxiv.org/html/2605.02163v1 , Sections III-B–III-C and
  Algorithm 1. A generator revises documentation using critic feedback.
  Generator–critic is an author-assigned descriptive label supported by this flow.
- Agentic RAG: https://doi.org/10.7717/peerj-cs.3642 , Agentic RAG workflow,
  Algorithm 1 and Knowledge Base Routing. A RouterAgent selects a specialized
  retriever using metrics and model reasoning. Router-based agentic is supported.

Publisher full-page access for MPC-Coder and PeerJ returned 403/429; indexed
full-text sections from those same publisher URLs were readable. The DocSync
author preprint was directly readable. These checks do not compare performance
across the studies or claim their terminology is identical to the table labels.
No related-work text or table cell needed changing in the manuscript.
