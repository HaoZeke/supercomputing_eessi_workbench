---
title: "Nodes, tasks, and threads"
teaching: 20
exercises: 20
---

::: callout
## TODO(Rohit)

The license for this lesson is still open. The course README says the module was adapted from Introducción a la Supercomputación by José Luis Bosque, Borja Pérez, Ramón Beivide, and Carmen Martínez of the Universidad de Cantabria, by the EuroCC NL team at SURF. Keep that attribution. Do not treat it as permission to republish the text under CC-BY until the license is confirmed.
:::

::: questions

- Which Slurm option is a node, a task, a core, and a thread?
- How many hostname lines does one node print when four tasks run there?

:::

::: objectives

- Map nodes, tasks, cores, and threads to `--nodes`, `--ntasks`, `--ntasks-per-node`, and `--cpus-per-task`.
- Load `2025` and `foss/2025a` inside a job and run `mpicc -v`.
- Predict the hostname lines for 2 nodes, 8 tasks, and 4 tasks per node.
- Use the course-cluster override `--nodes=3 --ntasks=6 --ntasks-per-node=2` when the nodes are small.

:::

## Four words, four options

A node is one computer. A task is one MPI rank. A core is one hardware processor reserved for that rank. A thread is one OpenMP thread inside the rank. Slurm does not count threads. It counts cores, and you point the threads at those cores.

| You mean | Option |
| --- | --- |
| How many computers | `--nodes` |
| How many MPI ranks in the job | `--ntasks` |
| How many of those ranks on each computer | `--ntasks-per-node` |
| How many cores for each rank | `--cpus-per-task` |

`--cpus-per-task` is the shared-memory side. The hybrid scripts set `OMP_NUM_THREADS` from `SLURM_CPUS_PER_TASK`. One core gives the rank one thread. Sixteen threads need `--cpus-per-task=16` on a node that has the cores.

`sbatch` reserves the allocation and runs your shell script. It does not launch the ranks. `srun` launches them. `squeue` shows the queue, `scancel` removes a job, and `sinfo` shows the nodes.

## What the published scripts ask for

The scripts under `episodes/files/hands-on/` are the Snellius requests. The sequential scripts ask for one task and `--cpus-per-task=16`. The hybrid scripts ask for `--ntasks=128` and `--cpus-per-task=1` on one node. Keep those lines on Snellius.

The smallest allocation and the partition name are in the tabs. Do not edit the scripts to change them. Options on the `sbatch` command line override the `#SBATCH` lines.

::: sites cpu-minimum
:::

::: sites partition-request
:::

::: sites scale-two-core
:::

On the course cluster the hostname exercise is `--nodes=3 --ntasks=6 --ntasks-per-node=2`. That is two tasks on each of three nodes.

## Load the compiler inside the job

The stack module differs by machine. Use the tab, then load the compiler toolchain the scripts use.

::: sites module-init
:::

:::: challenge
## Load `foss/2025a` in a job

Write `load_modules.sh` and submit it with `sbatch load_modules.sh`.

```bash
#!/bin/bash
#SBATCH -J load_modules
#SBATCH -o load_modules.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH -t 01:00:00

module load 2025
module load foss/2025a

echo "Loaded modules:"
module list

echo "Checking compiler version:"
mpicc -v
```

After the job finishes, `cat load_modules.out`. What shows that the compiler module is loaded?

::: solution
## Solution

The file lists the loaded modules, including `foss/2025a`, and then the version text from `mpicc -v`. A login-node `module list` is not that file. The job has its own environment. Add the partition line from the partition tab if the job waits with an invalid partition.
:::
::::

## Where `hostname` runs

`hostname` prints the name of the computer the task is on. One task on one node prints one line. The sample script spreads eight tasks across two nodes, four per node.

```bash
#!/bin/bash
#SBATCH -J name
#SBATCH -o name.out
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=4
#SBATCH -t 01:00:00

srun hostname
```

:::: challenge
## Four lines per host

The script asks for 2 nodes, 8 tasks, and 4 tasks per node. How many lines in `name.out` name each host? How many lines are there in total?

::: solution
## Solution

Four lines per host. Each node runs four tasks, and each task runs `hostname` once, so that host name appears four times. Two hosts give eight lines. The lines from the two hosts can be mixed in the file. The names are compute nodes.

On the course cluster, submit the same script with `--nodes=3 --ntasks=6 --ntasks-per-node=2`. Three hosts, two tasks on each, so two lines per host and six lines in total.
:::
::::

::: callout
## Ethernet and InfiniBand

Snellius connects nodes with InfiniBand. The course machines connect them with Ethernet. A job that spans nodes scales more weakly on the course machines than the same job on Snellius.
:::

::: keypoints

- `--nodes`, `--ntasks`, `--ntasks-per-node`, and `--cpus-per-task` are the node, the ranks, the ranks per node, and the cores (threads) per rank.
- `sbatch` reserves resources. `srun` starts the tasks.
- `module load 2025` and `module load foss/2025a` belong in the job. `mpicc -v` shows the compiler the job loaded.
- Eight tasks with four per node print four hostname lines for each of two hosts.
- The course-cluster hostname override is `--nodes=3 --ntasks=6 --ntasks-per-node=2`.

:::
