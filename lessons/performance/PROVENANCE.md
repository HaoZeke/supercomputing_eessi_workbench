# Provenance

The teaching follows `course-module-performance-analysis/slides/performance-analysis.org`
on branch `fix/slides-performance-source` at
`30f071f4fb6de454923c0c86676563344879b6ad`.

The deck is by Maxim Masterov (15.05.2025), adapted and updated by Rohit Goswami.

`episodes/fig/roofline.svg`, `episodes/fig/roofline-dark.svg`, and
`episodes/fig/roofline.png` are copied from the workbench `episodes/fig/`
directory.

The strong-scaling table with 8-core efficiency 0.625 is the worked series
in the workbench episode `episodes/performance-first-steps.md`. It is not
an AXPY measurement.

The arithmetic intensity in the roofline episode is the deck's example:
throughput 6.7257, bandwidth 2.6767, AI = 6.7257 / 2.6767 = 2.5 FLOP/byte.
