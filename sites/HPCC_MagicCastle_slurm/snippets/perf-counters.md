`perf stat` works when the host allows it. The client container has `perf` only if the host allows it.

```bash
perf stat -e cycles,instructions ./matmul 1000
```
