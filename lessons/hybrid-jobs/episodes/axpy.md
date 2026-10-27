---
title: "AXPY"
teaching: 15
exercises: 25
---

::: questions

- Why does AXPY speed up and then flatten?
- What does the hybrid program print for `y[0]` and for the local length?

:::

::: objectives

- Run the sequential AXPY in `hands-on/ex1` and the hybrid AXPY in `hands-on/ex2`.
- Match `y[0]` to `2 + 100 * 2 * 1`.
- Time 2, 4, and 8 tasks at a fixed vector length.
- On two-core nodes, submit with `sbatch --cpus-per-task=1 submit-axpy.sh 10000000` and `sbatch --ntasks=2 submit-axpy-hybrid.sh 10000000`.

:::

## Pointwise, and limited by bandwidth

AXPY is `y = a * x + y`. Each element is `y[i] = a * x[i] + y[i]`. No element waits on another, and the loop sends no messages. The work is one multiply and one add per element, and the bytes moved are the vectors. The run hits memory bandwidth early, so adding tasks stops shortening the time. That flattening is the result you are looking for. This episode does not give you a filled speedup table. You record the times.

Work in `episodes/files/hands-on/ex1` and `ex2`. `N` is the global length. Options you pass to `sbatch` override the `#SBATCH` lines.

## Sequential AXPY

`hands-on/ex1/axpy.c` fills `x` with 1 and `y` with 2, sets `a` to 2, and calls the loop 100 times. The script compiles and runs it like this:

```bash
gcc -O2 axpy.c -o axpy.out
```

```bash
srun ./axpy.out $N
```

Submit from the `ex1` directory:

```bash
sbatch submit-axpy.sh 10000000
```

The published script asks for `--cpus-per-task=16`. On a two-core node:

```bash
sbatch --cpus-per-task=1 submit-axpy.sh 10000000
```

A recorded run for `N` = 10000000 printed this. Your time will differ. `y[0]` will not.

```text
Length of the arrays: 10000000
y[0] = 202.000000
Time taken for axpy execution: 0.963870 seconds
```

`y` starts at 2. Each of the 100 calls adds `a * x[i] = 2 * 1`. So `y[0] = 2 + 100 * 2 * 1 = 202`.

:::: challenge
## Predict `y[0]`, then time one run

Before you submit, write the value of `y[0]` for `N` = 10000000. Submit the sequential script. Which lines are fixed by the program, and which line is your measurement?

::: solution
## Solution

`y[0]` is 202. The length line is the `N` you passed. The time line is your measurement. A second submit can print a different time. It should print the same `y[0]`.
:::
::::

## Hybrid AXPY

`hands-on/ex2/axpy-hybrid.c` splits `N` across MPI ranks. If `N` divides evenly, each rank holds `N / ntasks` elements. Rank 0 prints that local length. Every rank fills its own arrays with the same 1 and 2, so `y[0]` on rank 0 is still 202. There is no halo and no reduction.

The OpenMP loop is the outer element loop on that rank:

```c
#pragma omp parallel for
for (size_t i = 0; i < local_n; i++) {
    y[i] = a * x[i] + y[i];
}
```

The script compiles and launches with:

```bash
mpicc -O2 -fopenmp axpy-hybrid.c -o axpy-hybrid.out
```

```bash
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
```

```bash
srun ./axpy-hybrid.out $N
```

The published script is `--nodes=1`, `--ntasks=128`, `--cpus-per-task=1`. A recorded run at `N` = 10000000 with those 128 tasks printed:

```text
Global length of the arrays: 10000000
Local length of the arrays: 78125
y[0] = 202.000000
Time taken for axpy execution: 0.009485 seconds
```

`10000000 / 128 = 78125`. That local length checks the split. Your time will differ. These two samples are separate recorded runs. Keep them out of a speedup series.

`Hyb-T-C` means T MPI tasks and C OpenMP threads. `sbatch --ntasks=1 --cpus-per-task=16 submit-axpy-hybrid.sh 10000000` is `Hyb-1-16` on a machine that can give you 16 cores.

::: callout
## Pin threads when a task has more than one

The published `ex2` script does not pin threads. When you give a task more than one thread, pin them so the operating system does not move them during the timed loop. Set this before `srun`:

```bash
export OMP_PLACES=cores
export OMP_PROC_BIND=close
srun --cpu-bind=cores ./axpy-hybrid.out $N
```

`OMP_PLACES=cores` gives each thread its own core. `OMP_PROC_BIND=close` keeps that task's threads on neighbouring cores. `--cpu-bind=cores` keeps each rank on the cores Slurm gave it.
:::

:::: challenge
## Time 2, 4, and 8 tasks

From `ex2`, at `N` = 10000000, record the time line for 2, 4, and 8 tasks, one thread per task:

```bash
sbatch --ntasks=2 --cpus-per-task=1 submit-axpy-hybrid.sh 10000000
sbatch --ntasks=4 --cpus-per-task=1 submit-axpy-hybrid.sh 10000000
sbatch --ntasks=8 --cpus-per-task=1 submit-axpy-hybrid.sh 10000000
```

On a two-core node the hybrid line that fits on one node is:

```bash
sbatch --ntasks=2 submit-axpy-hybrid.sh 10000000
```

Four and eight tasks need more cores than that node has. Use the course tab from the previous episode for the runs that fit, and do not edit the script.

What do you write down, and what shape do you expect from a bandwidth limit?

::: solution
## Solution

Write down the `Time taken for axpy execution` line, the task count, and `y[0]`. `y[0]` stays 202. The local length is `10000000` divided by the task count when the split is even: 5000000, 2500000, and 1250000.

The times should drop and then flatten. AXPY moves a lot of bytes per arithmetic operation, so extra tasks stop helping once the memory path is full. A time that stays flat when you double the tasks is the bandwidth limit. `y[0]` is the correctness check, and it stays 202.

On Snellius the published script's 128 tasks are one more column on the sheet. Still record 2, 4, and 8.
:::
::::

## A sheet for a full node

On Snellius you can also fill this sheet. Leave the cells empty until your jobs print a time. `Hyb-256-1` and `Hyb-2-128` need 256 cores, so they need `--nodes=2`. The script asks for one node.

```bash
sbatch --nodes=2 --ntasks=256 --cpus-per-task=1 submit-axpy-hybrid.sh <N>
sbatch --nodes=2 --ntasks=2 --cpus-per-task=128 submit-axpy-hybrid.sh <N>
```

The last row, `N` = 10000000000, needs about 160 GB for `x` and `y`. Add `--exclusive` so the job gets the memory of a full node.

| Vector size | Sequential | Hyb-16-1 | Hyb-128-1 | Hyb-256-1 | Hyb-1-16 | Hyb-1-128 | Hyb-2-128 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1,000,000 | | | | | | | |
| 10,000,000 | | | | | | | |
| 100,000,000 | | | | | | | |
| 1,000,000,000 | | | | | | | |
| 10,000,000,000 | | | | | | | |

On the course cluster, do not use those wide columns. The course tab lists `Hyb-2-1`, `Hyb-1-2`, `Hyb-3-2`, and `Hyb-6-1`, and it leaves out the two largest sizes.

After a job finishes you can read how the allocation was used:

```bash
seff JOBID
sacct -j JOBID --format=JobID,AllocCPUS,Elapsed,TotalCPU,MaxRSS,State
```

`seff` reports CPU time used, divided by allocated cores times elapsed time. The whole job is in that figure, including compilation. Compare two configurations. Do not treat one short run's percentage as the kernel's speedup.

::: keypoints

- AXPY is pointwise. The hybrid code has no reduction. Bandwidth limits it, so speedup flattens early.
- Sequential compile and run: `gcc -O2 axpy.c -o axpy.out` and `srun ./axpy.out $N`.
- Hybrid compile and run: `mpicc -O2 -fopenmp axpy-hybrid.c -o axpy-hybrid.out`, `export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK`, and `srun ./axpy-hybrid.out $N`.
- `y[0]` is 202 for this initialisation and 100 repetitions. The local length is the global length split across tasks.
- Two-core submissions: `sbatch --cpus-per-task=1 submit-axpy.sh 10000000` and `sbatch --ntasks=2 submit-axpy-hybrid.sh 10000000`.

:::
