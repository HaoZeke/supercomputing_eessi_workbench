---
title: "Slurm resources"
teaching: 10
exercises: 15
---

::: questions

- What does a job of 4 MPI ranks and 8 threads per rank ask for?
- What do `SLURM_NTASKS` and `SLURM_CPUS_PER_TASK` print?

:::

::: objectives

- Write `--nodes`, `--ntasks`, and `--cpus-per-task` for 4 ranks and 8 threads each.
- Check `SLURM_NTASKS` and `SLURM_CPUS_PER_TASK`, then run `seff JOBID`.
- State what `--exclusive`, `--sockets-per-node`, and `--gpus-per-node` request.

:::

## Nodes, tasks, and cores

`sbatch` does not launch tasks. It reserves an allocation and runs your script. The task options tell Slurm what the later `srun` will need.

- `--nodes` (or `-N`) is how many nodes.
- `--ntasks` (or `-n`) is the maximum number of tasks the steps in that allocation will launch. Slurm reserves enough resources for that many.
- `--ntasks-per-node` asks for that many tasks on each node.
- `--cpus-per-task` (or `-c`) is how many processors each task needs. Without it, Slurm tries to give one processor per task.

Threads are not a separate Slurm option. Eight OpenMP threads on a rank need `--cpus-per-task=8`, and the program should set `OMP_NUM_THREADS` from `SLURM_CPUS_PER_TASK`.

The smallest allocation and the partition are in the tabs. The published meaning of the three options above does not change. Whether one node can hold the total does.

::: sites cpu-minimum
:::

::: sites partition-request
:::

## Sockets, GPUs, and the shape of the allocation

- `--sockets-per-node` keeps the selection to nodes that have at least that many sockets.
- `--gpus-per-node` is how many GPUs the job needs on each node.
- `--contiguous` asks for nodes that form a contiguous set.
- `--exclusive` means the allocation cannot share its nodes with other running jobs.

## What the job records

- `SLURM_JOB_NODELIST` is the list of nodes allocated to the job.
- `SLURM_NTASKS` is the value of `--ntasks` when you set it. If you set `--ntasks-per-node` or `--ntasks-per-gpu` instead, it is the number of tasks in the job.
- `SLURM_CPUS_PER_TASK` is the cores requested per task. It is set when you pass `--cpus-per-task`.
- `SLURM_GPUS` is the number of GPUs requested. It is set only when you pass `-G` or `--gpus`.

:::: challenge
## Four ranks, eight threads

A program runs 4 MPI ranks with 8 threads each. Write `--nodes`, `--ntasks`, and `--cpus-per-task`. Submit a script that prints the two variables, then run `seff` on the job id.

```bash
#!/bin/bash
#SBATCH --job-name=four-eight
#SBATCH --time=00:10:00
#SBATCH --output=four-eight-%j.out

echo "SLURM_NTASKS=$SLURM_NTASKS"
echo "SLURM_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK"
```

Add your three resource lines, and the partition line from the partition tab. What should the file contain?

::: solution
## Solution

The program is 4 ranks and 8 cores per rank:

```bash
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=8
```

`4 * 8 = 32` cores. `--nodes=1` is right when one node can hold 32 cores. You do not have to set `--ntasks-per-node` as well: one node and four tasks already places four tasks on that node.

`SLURM_NTASKS` prints 4. `SLURM_CPUS_PER_TASK` prints 8 when `--cpus-per-task=8` is set. Omit that option and Slurm tries to allocate one core per task.

If the cpu-minimum tab shows a node smaller than 32 cores, that node cannot take this request unchanged. The tab is where that limit is written. Do not invent a second core count in the script.

```bash
seff JOBID
```

`seff` reports CPU time used, divided by allocated cores times elapsed time. This script only prints two lines, so the figure covers a tiny amount of work. Read it as a check that the allocation was 32 cores (`4 * 8`).
:::
::::

## Billing units

A 16-core job's system billing units are on the accounting tab. That tab already has the arithmetic.

::: sites accounting
:::

::: keypoints

- 4 MPI ranks and 8 threads each is `--ntasks=4` and `--cpus-per-task=8`. `--nodes=1` when the node can hold 32 cores.
- `SLURM_NTASKS` is 4 and `SLURM_CPUS_PER_TASK` is 8 when those options are set.
- Without `--cpus-per-task`, Slurm tries to allocate one processor per task.
- `--exclusive` does not share nodes. `--sockets-per-node` and `--gpus-per-node` constrain sockets and GPUs. `--contiguous` asks for a contiguous set of nodes.
- `seff JOBID` is CPU time used, divided by allocated cores times elapsed time. Billing units are the accounting tab.

:::
