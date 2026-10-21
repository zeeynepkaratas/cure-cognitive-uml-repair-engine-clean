# Versioned structural metrics

The historical heuristic is available as calculate_semantic_fidelity_legacy or
legacy=True. It retains the relationship-default credit that produces .25 on
S02. It must not be mixed with v2 values or described as an ISO-defined metric.

For v2 use case-folded source class set S and diagram class set U. Missing
classes M=S−U; unsupported classes H=U−S. Completeness C=1−|M|/|S|;
consistency K=1−|H|/|U|, with K=1 if U is empty. If S is empty, the score is
null and status is not_applicable; there is no pass/fail interpretation.

When source edges exist, score=.35*class_F1+.25*directed_pair_F1+.25*C+.15*K.
When no source edges exist, omit that term and divide the other terms by .75.
Full precision is used internally; display fields may be rounded. This is a
project-specific structural agreement proxy, not semantic correctness.

The default SRS extractor is a limited lexical proper-name heuristic. A supplied
EntityExtractor can substitute a manually curated reference model; such gold
data is used for evaluation only and must never be passed to repair agents.
Modern STOP_WORDS share one module; legacy copies are frozen for reproduction.
