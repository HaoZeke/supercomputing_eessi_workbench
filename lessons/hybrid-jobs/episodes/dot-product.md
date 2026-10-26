---
title: "Dot product"
teaching: 15
exercises: 25
---

::: questions

- Where is the reduction in the hybrid dot product?
- Why can the last digits differ when the printed value matches?

:::

::: objectives

- Run the sequential dot product in `hands-on/ex3` and the hybrid program in `hands-on/ex4`.
- Find the OpenMP `reduction(+:)` clause and the MPI reduction.
- Time 2, 4, and 8 tasks at a fixed length.
- On the course cluster, submit `sbatch --nodes=3 --ntasks=6 submit-dot-hybrid.sh 30000000`.

:::

## A pointwise product, then a sum

The dot product is the sum of `x[i] * y[i]`. Each product is independent. The sum is not. Someone has to add the partial sums. That add is the reduction.

In `hands-on/ex3/dot.c` the vectors are `sin(i)` and `0.5 * cos(i)`. The program adds the dot product into `result` over 100 repetitions. The script compiles and runs:

```bash
gcc -O2 dot.c -o dot.out -lm
```

```bash
srun ./dot.out $N
```

```bash
sbatch submit-dot.sh 10000000
```

On a two-core node:

```bash
sbatch --cpus-per-task=1 submit-dot.sh 10000000
```

A recorded run for `N` = 10000000 printed:

```text
Length of the arrays: 10000000
Dot product result: 12.3778
Time taken for dot product execution: 1.21664 seconds
```

Your time will differ. The result line is the value to compare with the hybrid run.

## Two reductions

`hands-on/ex4/dot-hybrid.c` gives each rank a slice of the global index, stored in `offset`, so `sin` and `cos` see the same `i` as the sequential loop. The live OpenMP loop is:

```c
#pragma omp parallel for reduction(+:local_sum)
for (size_t i = 0; i < local_n; i++) {
    local_sum += x[i] * y[i];
}
```

`reduction(+:local_sum)` gives each thread a private sum and adds those private sums at the end of the loop. The file also contains a commented loop that splits the iterations by hand. The live function is the reduction clause.

Each rank then needs a global sum. The call in the timed loop is `MPI_Allreduce` with `MPI_SUM`:

```c
MPI_Allreduce(&local_result, &global_result, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
result += global_result;
```

`MPI_Reduce` would leave the sum on one rank. `MPI_Allreduce` is that reduction with the sum delivered to every rank. This file uses `MPI_Allreduce` because every rank adds `global_result` into `result`. Rank 0 prints `result`. The collective sits inside the 100 repetitions, so the printed time includes it.

The script compiles and launches with:

```bash
mpicc -O2 -fopenmp dot-hybrid.c -o dot-hybrid.out -lm
```

```bash
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
```

```bash
srun ./dot-hybrid.out $N
```

A recorded run at `N` = 10000000 with the script's 128 tasks printed:

```text
Global length of the arrays: 10000000
Local length of the arrays: 78125
Global dot product result: 12.3778
Time taken for dot product execution: 0.039711 seconds
```

The result matches the sequential run to the digits that were printed. The order of the additions is different, so later digits can differ. As with AXPY, do not turn these two sample times into a speedup table.

When a task has more than one thread, pin them the same way as in the AXPY episode: `OMP_PLACES=cores`, `OMP_PROC_BIND=close`, and `srun --cpu-bind=cores`.

:::: challenge
## Name the reductions, then time the tasks

In `dot-hybrid.c`, which OpenMP clause combines the thread sums, and which MPI call combines the rank sums?

Then, from `ex4`, record the time at `N` = 10000000 for 2, 4, and 8 tasks:

```bash
sbatch --ntasks=2 --cpus-per-task=1 submit-dot-hybrid.sh 10000000
sbatch --ntasks=4 --cpus-per-task=1 submit-dot-hybrid.sh 10000000
sbatch --ntasks=8 --cpus-per-task=1 submit-dot-hybrid.sh 10000000
```

On the course cluster the run that matches the override table is:

```bash
sbatch --nodes=3 --ntasks=6 submit-dot-hybrid.sh 30000000
```

What local length should rank 0 print for that course command? What result digits should match the sequential run?

::: solution
## Solution

The OpenMP clause is `reduction(+:local_sum)`. The MPI call is `MPI_Allreduce` with `MPI_SUM`. That is a reduction. `MPI_Reduce` is the form that keeps the sum on one rank. This file uses the all-ranks form.

The course command runs 6 tasks and `N` = 30000000. `30000000 / 6 = 5000000`, and 6 divides 30000000, so rank 0 prints local length 5000000.

Compare `Global dot product result` with a sequential run at the same `N`. The printed digits should match. Digits past what `%g` showed can move, because the sum is associated differently. The time includes 100 global reductions, so this kernel has a communication cost that AXPY does not. Extra tasks still help the products, and the reduction grows with the task count. Record the times. Do not expect them to halve forever.

Four and eight tasks on one two-core node do not fit. The six-task line above is the course override. It uses three nodes. Cross-node scaling on Ethernet is weaker than on InfiniBand. Keep a course three-node time in the course column.
:::
::::

## The same sheet, still empty

On Snellius the recording sheet has the same columns as AXPY. Fill it with your times. `Hyb-256-1` and `Hyb-2-128` need `--nodes=2`:

```bash
sbatch --nodes=2 --ntasks=256 --cpus-per-task=1 submit-dot-hybrid.sh <N>
sbatch --nodes=2 --ntasks=2 --cpus-per-task=128 submit-dot-hybrid.sh <N>
```

The last row needs about 160 GB for `x` and `y`. Add `--exclusive` for that row.

| Vector size | Sequential | Hyb-16-1 | Hyb-128-1 | Hyb-256-1 | Hyb-1-16 | Hyb-1-128 | Hyb-2-128 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1,000,000 | | | | | | | |
| 10,000,000 | | | | | | | |
| 100,000,000 | | | | | | | |
| 1,000,000,000 | | | | | | | |
| 10,000,000,000 | | | | | | | |

On the course cluster, use `Hyb-2-1`, `Hyb-1-2`, `Hyb-3-2`, and `Hyb-6-1`, and leave out the two largest sizes. The six-task command in the challenge is `Hyb-6-1` at `N` = 30000000.

::: keypoints

- The products are independent. The sum is a reduction.
- OpenMP uses `reduction(+:local_sum)`. MPI uses `MPI_Allreduce` with `MPI_SUM`, the all-ranks form of `MPI_Reduce`.
- Compile and run with `mpicc -O2 -fopenmp dot-hybrid.c -o dot-hybrid.out -lm`, `export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK`, and `srun ./dot-hybrid.out $N`.
- The printed result matches the sequential digits. Later digits can differ because the add order differs.
- The course command is `sbatch --nodes=3 --ntasks=6 submit-dot-hybrid.sh 30000000`.

:::
