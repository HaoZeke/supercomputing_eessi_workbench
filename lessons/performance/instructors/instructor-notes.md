---
title: Instructor notes
---

## Timing

| Episode | Teaching | Exercises |
| --- | --- | --- |
| How to evaluate a run | 15 | 5 |
| What limits a run | 20 | 10 |
| Strong and weak scaling | 15 | 20 |
| The roofline | 25 | 20 |
| Energy | 10 | 10 |
| Slurm resources | 10 | 15 |

## What to cut

The energy episode is the first to cut. EAR and `eacct` exist on Snellius. The course tab says to skip them.

## Numbers you may quote

The 8-core efficiency 0.625 comes from the worked series 8.0 seconds on 1 core and 1.6 seconds on 8 cores. Show `8.0 / (8 * 1.6)`. Keep that series separate from any AXPY times the room records.

The roofline example is throughput 6.7257 and bandwidth 2.6767, so AI = 6.7257 / 2.6767 = 2.5 FLOP/byte. Do not substitute a different arithmetic intensity. The deck does not give a numeric ridge. Learners compare 2.5 with the ridge of the machine they measured.

The AXPY binary is in the hybrid-jobs lesson. Do not paste a second `axpy.c` into this lesson.

## Sam

Sam wants a number for whether more cores helped. Give Sam speedup `T(1) / T(N)` and efficiency `T(1) / (N * T(N))`. A shorter `real` time means the run finished sooner. Efficiency is how much of the added cores showed up in that time.

## Tabs

The course cluster is a SURF Research Cloud workspace, and the course tab requests `--partition=rome`. Counters on the course cluster are `perf` and PAPI, not uProf. Billing units, if anyone asks, are the accounting tab. Do not put a second copy of that formula on the board.
