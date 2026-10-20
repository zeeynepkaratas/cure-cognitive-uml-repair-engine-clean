# Submission audit 2026-10-20

This audit reads retained experiment outputs and measures no-repair inputs
locally. The measurement did not rerun an LLM, change application code, change
retained experimental outputs, or move the original submission tag. Its
evidence is published separately as a documentation update. The baseline is a
later measurement, not part of the original retained LLM runs.

## Evidence

- `cases.csv`: 120 retained case/method records, including raw timing field names.
- `baseline_none.csv`: all 60 unmodified shared/PURE inputs.
- `baseline_runtime_raw.json`: original per-case validator/compiler results.
- `audit_results.json`: matrices, differences, descriptive statistics, counts.
- `pure_counts.csv`: reference and output graph sizes.
- `pure_license_record.json`: upstream license declaration and requested citation.
- `cure_audit.py`, `cure_verify.py`, `mcnemar_exact.py`: original local audit scripts.
  These retain the audit machine's absolute paths and need path adaptation on
  another machine; they are evidence of the calculation, not portable CLIs.
- `audit_stdout.txt`: original calculation output.

The compiler check calls the repository's `validate_with_plantuml` helper,
which runs `java -jar <jar> -tsvg -checkonly <temporary-input>` with timeout 20 s.
The local JAR reports 1.2026.6; SHA-256 is
`89948F14C93756C7A3FB7B69078FF37E8489FD79DD430C582B931E2F65358690`.
The baseline does not alter or repair its inputs. SciPy 1.18.1 exact paired
tests use `binomtest(b, b+c, p=0.5, alternative="two-sided")`; this is the exact
McNemar test on discordant pairs. Zero discordant pairs imply p=1.
Tests are exploratory, without multiplicity adjustment.

The no-repair compilation totals are 12/50 and 2/10; both project totals are 0.
Shared paired tables (rows deterministic pass/fail; columns LLM pass/fail):
compilation `[[33,8],[7,2]]`, project `[[30,1],[19,0]]`.
The exact p-values are 1.0 and 0.0000400543212890625.

Remaining limits: original PURE document filenames/number used are unresolved;
single-pass LLM and Healer-without-Critic ablations were not run. No claim of
LLM superiority or isolated component contribution follows from these results.
