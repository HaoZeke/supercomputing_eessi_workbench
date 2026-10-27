uProf and `--constraint=hwperf` are Snellius only. On this cluster, PAPI and `perf` read the counters.

```bash
perf stat -e cycles,instructions ./matmul 1000
```
