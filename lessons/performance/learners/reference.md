---
title: Glossary
---

## Glossary

wall-clock time
: The `real` line from `time -p`. The seconds you waited.

strong scaling
: The problem size stays fixed and the number of processors grows. Speedup is `T(1) / T(N)`.

weak scaling
: The problem size grows with the number of processors, so each processor keeps about the same work.

speedup
: `T_s / T_N`. `T_s` is the serial time. `T_N` is the time on N processors.

efficiency
: `T_s / (N * T_N)`. The worked 8-core value in this lesson is 0.625.

Amdahl's law
: Strong-scaling speedup is `1 / (s + p/N)`. `s` is the serial share of the time, `p` is the parallel share, `N` is the number of processes.

Gustafson's law
: Weak-scaling speedup is `s + p*N`. The parallel share grows with the resources. The serial share stays fixed as the problem grows.

arithmetic intensity
: Floating-point operations per byte moved. The unit is FLOP/byte.

ridge point
: The arithmetic intensity where the bandwidth roof meets the peak roof.

roofline
: A plot of performance against arithmetic intensity, under the bandwidth roof and the peak roof.

memory-bound
: Left of the ridge. The kernel waits on bytes moving.

compute-bound
: Right of the ridge. The kernel waits on arithmetic peak.

FLOP
: One floating-point operation. An add is 1 FLOP. A multiply is 1 FLOP.

EAR
: Energy Aware Runtime on Snellius. `--ear=on` and `--ear-policy=monitoring`, then `eacct -j JOBID`.

## Tools from the deck

| Tool | Cost | Description |
| --- | --- | --- |
| Linaro DDT | Non-free | Full featured graphical, parallel debugger |
| HPCToolkit | Free | Integrated suite of tools for parallel program performance analysis |
| Intel One API | Free, with conditions | Stack of performance analysis and debugging tools (MPI/OpenMP/SIMD) |
| Valgrind | Free | Memory errors debugging tool |
| TotalView | Non-free | Full featured graphical, parallel debugger |
| Vampir | Non-free | Full featured trace visualizer for parallel program OTF trace files |
| memP | Free | Lightweight memory profiling tool |
| mpiP | Free | Lightweight MPI profiling tool |
| PAPI | Free | A standardized and portable API for accessing performance counter hardware |
| likwid | Free | A tool to measure hardware performance counters |
| Tau | Free | Full featured parallel program performance analysis toolkit |
| Extrae | Free | MPI/OpenMP profiler |
| Scalasca | Free | MPI+OpenMP analysis with Score-P (Score-P/9.2-gompi-2025a) |
| Darshan | Free | IO profiler |
| Nsight | Free | GPU: nsys (Nsight-Systems/2025.4.1), ncu (CUDA/12.8.0) |
| Linaro MAP | Non-free | Performance analysis tool for MPI+OpenMP |
| uProf | Free | AMD CPU counters, sampling, and roofline analysis |
| gprof | Free | Standard unix/linux profiling utility |

The course cluster tab in the roofline episode uses `perf` and PAPI. uProf is the Snellius example in the deck.
