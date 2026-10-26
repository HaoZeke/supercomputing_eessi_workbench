---
title: Glossary
---

## Glossary

node
: One computer in the cluster. `--nodes` is how many you ask for.

task
: One MPI rank. `--ntasks` is how many ranks the job may launch. `srun` starts them. `sbatch` only reserves the allocation.

thread
: One OpenMP thread inside a rank. The hybrid scripts set `OMP_NUM_THREADS` from `SLURM_CPUS_PER_TASK`.

core
: A hardware processor. `--cpus-per-task` is how many cores Slurm reserves for the threads of one task.

AXPY
: The update `y = a * x + y`, applied element by element. There is no reduction.

dot product
: The sum of `x[i] * y[i]`. The hybrid program reduces that sum with OpenMP and with MPI.

reduction
: Combining partial sums into one sum. In this lesson the OpenMP clause is `reduction(+:)` and the MPI call is `MPI_Allreduce` with `MPI_SUM`, the all-ranks form of `MPI_Reduce`.

checksum
: The sum of every entry of `C` after matrix multiplication. The program prints it as `Matrix checksum:` with `%.17g`. Same `n`, same line.

InfiniBand
: The network that connects Snellius compute nodes. The course machines use Ethernet, so a job that crosses nodes scales more weakly there.
