---
title: "Python and OpenMP on a node"
teaching: 10
exercises: 25
---

::: questions
- What sum does `python.sh` print, and which modules does the script load?
- Why does every line of `pi.sh` report the same `pi`, with a different thread count?
- What do you pass to `sbatch` on a two-core node, without editing the script?
:::

::: objectives
- Submit the published Python script and check the sum `499999500000`.
- Build the OpenMP pi program and read `pi = 3.141592654` for each thread count the allocation allows.
- Leave `#SBATCH --partition=rome` in the published scripts, and override the core count on the `sbatch` command when the node is small.
:::

## Two published scripts

The files are in `episodes/files/hands-on/`. They are the batch examples from the fundamentals deck. Run them from that directory. Both scripts set `#SBATCH --partition=rome`. Leave that line. The site tab says what to do on the machine in your welcome note.

::: sites partition-request
:::

## A Python sum

`python.sh` asks for one node, one task, and two minutes. It loads the 2025 stack and `Python/3.13.1-GCCcore-14.2.0`, then runs:

```bash
srun python3 -c 'import platform; print("Python on", platform.node()); print("sum:", sum(range(1000000)))'
```

`sum(range(1000000))` is the sum of 0 through 999999. That sum is `499999500000`. The node name on the first line is whatever node Slurm gave the job.

```bash
sbatch python.sh
```

The version string in this script is `Python/3.13.1-GCCcore-14.2.0`. The modules episode loads `Python/3.13.5-GCCcore-14.3.0` from the current stack. They are different lines. Use the line that is in the file you submit.

:::::::::::: challenge
## What is the sum?

Without running the job, what does `sum(range(1000000))` print? After the job finishes, where do you read that number?

:::::: solution
## Solution

`499999500000`.

The formula for the sum of `0 .. n-1` is `n*(n-1)/2`. With `n = 1000000` that is `1000000*999999/2 = 499999500000`.

Slurm writes the script's stdout to `slurm-<jobid>.out` in the directory where you ran `sbatch`. The line starts with `sum:`.
::::::
::::::::::::

## OpenMP pi

`pi.c` integrates `4/(1+x^2)` from 0 to 1 with the midpoint rule, `100000000` steps. The loop is `#pragma omp parallel for reduction(+:sum)`. Each rank of the loop adds into a private sum, and OpenMP adds those into one `sum` at the end. The print is:

```text
pi = 3.141592654; threads = N; elapsed = ... s
```

`%.9f` is why you see nine digits. Every thread count should print `pi = 3.141592654`. The elapsed time is the thing that changes, and a short loop can spend a visible fraction of that time just starting the threads.

`compilepi` loads `module load 2025` and `module load GCC/14.2.0`, then:

```bash
gcc -O3 -fopenmp -Wall -Wextra pi.c -o pi
```

`pi` is that binary. It is not a module.

`pi.sh` asks for one node, one task, 32 CPUs, and ten minutes, on `rome`. It loads the same GCC module and loops:

```bash
for ncores in 1 2 4 8 16 32; do
    if (( ncores <= SLURM_CPUS_PER_TASK ))
    then
        export OMP_NUM_THREADS=$ncores
        srun --cpu-bind=cores ./pi
    fi
done
```

A thread count above `SLURM_CPUS_PER_TASK` is skipped. On the published 32-CPU request you get six lines. Compare each elapsed time with the one-thread line. Speedup for this short integral is often poor: the loop is not long enough to hide the cost of starting more threads.

```bash
bash compilepi
sbatch pi.sh
```

## A two-core node

The published scripts stay as they are, including `--cpus-per-task=32` and `--partition=rome`. On a small node you pass the smaller request on the `sbatch` command. That overrides the line in the file.

::: sites scale-two-core
:::

On the course cluster the pi override is:

```bash
sbatch --cpus-per-task=2 pi.sh
```

Check `sinfo` before you quote a core count in the room.

:::::::::::: challenge
## How many lines?

`pi.sh` loops over 1, 2, 4, 8, 16, and 32 threads, and skips a count that is larger than `SLURM_CPUS_PER_TASK`.

1. How many `pi =` lines do you get from `sbatch pi.sh` on a node that honours `--cpus-per-task=32`?
2. How many do you get from `sbatch --cpus-per-task=2 pi.sh`?
3. Which digits of pi should differ between those lines?

:::::: solution
## Solution

1. Six lines: 1, 2, 4, 8, 16, and 32.
2. Two lines: 1 and 2. The test `ncores <= SLURM_CPUS_PER_TASK` drops 4, 8, 16, and 32.
3. None. Each line should report `pi = 3.141592654`. Threads and elapsed time change. The integral does not.

::::::
::::::::::::
