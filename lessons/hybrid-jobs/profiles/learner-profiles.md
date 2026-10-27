---
title: Learner profiles
---

## Idris

Idris requests one core and 16 threads. The request is `--cpus-per-task=1` together with an expectation of 16 OpenMP threads. The hybrid scripts set `OMP_NUM_THREADS` from `SLURM_CPUS_PER_TASK`, so that request is one thread. Exporting `OMP_NUM_THREADS=16` on top of one core makes the 16 threads share that core. The threads run at the same time only when the core count is at least the thread count. On a two-core node, use the course tab.
