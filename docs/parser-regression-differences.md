# Parser compatibility check

All 120 retained final outputs are compared against the explicit legacy parser.
One malformed declaration has a corrected class set: shared deterministic S46,
legacy {class}, current {GeneratedDiagram}. The old regex crosses a newline
after a nameless class token and mistakes the next keyword for a class name.
This additional defect is recorded as F19. Legacy parsing remains available;
retained measurements are not rewritten. This is an intentional correction,
not evidence that historical semantic scores can be compared with v4 scores.

Current relationship parsing also supports realization, short arrows, styled
arrows, true arrow direction, self-relations and undirected dependencies.
The v4 runner computes those metrics afresh and records its parser version.
