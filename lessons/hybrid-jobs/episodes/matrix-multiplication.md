---
title: "Matrix multiplication"
teaching: 10
exercises: 30
---

::: questions

- What has to stay the same when you parallelise the outer loop?
- Which compile flag makes the pragma real?

:::

::: objectives

- Run `hands-on/ex5` at sizes 500, 1000, and 2000.
- Read `Matrix checksum:` and see that the same size prints the same line.
- Parallelise the outer loop with OpenMP without changing that checksum.

:::

## One product, then a sum of the entries

`hands-on/ex5/matmul.c` computes `C = A * B` for square `n` by `n` matrices. For each `i` and `j` it dots row `i` of `A` with column `j` of `B`. It does this 100 times. Each repetition overwrites `C`. The checksum runs after that loop, so it sums the last product. The 100 repetitions overwrite `C`.

`A` is filled with 1 and `B` with 2. Each entry of `C` is `2 * n`. The checksum adds every entry, so it is `2 n^3`. It depends only on `n`. Two runs with the same `n` print the same `Matrix checksum:` line. The printf is `Matrix checksum: %.17g`.

The script compiles and runs:

```bash
gcc -O2 matmul.c -o matmul.out
```

```bash
srun ./matmul.out $N
```

The published request is one task and `--cpus-per-task=16`. On a two-core node, size 500 is:

```bash
sbatch --cpus-per-task=1 submit-matmul.sh 500
```

:::: challenge
## Same size, same checksum

From `ex5`, run sizes 500, 1000, and 2000. Run 500 twice.

```bash
sbatch submit-matmul.sh 500
sbatch submit-matmul.sh 500
sbatch submit-matmul.sh 1000
sbatch submit-matmul.sh 2000
```

On a two-core node start with `sbatch --cpus-per-task=1 submit-matmul.sh 500`.

What is `Matrix checksum:` for `n` = 500, and what must the second run print?

::: solution
## Solution

`2 * 500^3 = 250000000`. The line is `Matrix checksum: 250000000`. The second run with `n` = 500 prints that same line. `n` = 1000 prints `2000000000`. `n` = 2000 prints `16000000000`.

The time line is your measurement. The checksum is the correctness check. The script's time limit is one hour. If a larger size is still running at that limit, the job ends. That does not change the checksum of a run that finished.
:::
::::

## Parallelise the outer loop

There is no hybrid matrix program in the hands-on set. The open exercise is to parallelise `matmul` with OpenMP.

The outer loop is the `i` loop. Row `i` of `C` is only written by that iteration. `A` and `B` are only read. Threads that each own a different `i` do not write the same entry. The `j` and `k` loops stay inside the thread, so each entry is still a serial dot product. The checksum loop stays serial, after the parallel loop, so it adds the entries in the same order.

The finished file is `episodes/files/solutions/matmul-omp.c`. Try the change yourself before you read it.

:::: challenge
## OpenMP on the `i` loop

Copy `matmul.c` and add OpenMP on the outer loop only. Build with `-fopenmp`. The published `gcc` line has no OpenMP flag, so a pragma in the source does nothing until you change the compile line:

```bash
gcc -O2 -fopenmp matmul-omp.c -o matmul.out
```

Set the thread count from the allocation, as the hybrid scripts do:

```bash
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
```

Run the same `n` as the sequential checksum. What must `Matrix checksum:` do?

One core and 16 threads do not run 16 ways at once. `--cpus-per-task` is the number of cores. Match it to the thread count on a node that has the cores. The checksum check itself does not need 16 cores.

::: solution
## Solution

The pragma is on the outer loop:

```c
#pragma omp parallel for
for (size_t i = 0; i < n; i++) {
```

That is the change in `episodes/files/solutions/matmul-omp.c`, plus `#include <omp.h>`. The `printf` is still `Matrix checksum: %.17g`.

For a given `n`, the checksum line matches the sequential run. For `n` = 500 that is `250000000`. A different checksum means two iterations wrote the same `C[i][j]`, or the inner dot product changed. The time line in this file comes from `clock`, which reports CPU time. Use the checksum to decide if the parallel loop is right.
:::
::::

::: keypoints

- `C[i][j]` is `2 * n` for these inputs, and `Matrix checksum:` is `2 n^3`.
- The same `n` prints the same checksum. The printf format is `%.17g`.
- The sequential compile and run lines are `gcc -O2 matmul.c -o matmul.out` and `srun ./matmul.out $N`.
- The course size-500 line is `sbatch --cpus-per-task=1 submit-matmul.sh 500`.
- Parallelise the outer `i` loop with `#pragma omp parallel for`, compile with `-fopenmp`, and leave the checksum unchanged.

:::
