---
title: "Embarrassingly parallel"
teaching: 15
exercises: 0
---

::: questions

- What is an embarrassingly parallel workload on a dense node?
- Why does one Slurm job per short command waste the scheduler?

:::

::: objectives

- Describe a workload of many independent tasks that share a node badly if each task is its own job.
- Name the three families on the deck: background processes with `numactl`, Slurm arrays, and a service inside one allocation.
- Name QCG-PilotJob, HyperQueue, Snakemake, and FireWorks as the tools the last episode compares.

:::

## Many independent tasks

An embarrassingly parallel workload runs many independent small jobs at the same time, so the node stays busy.

You reach for that pattern in three situations.

- The runs cannot be combined into a single application.
- A large parameter sweep uses the same application, or a workflow whose pipeline steps depend on each other.
- A step depends on software that stops scaling past some number of cores.

Nodes are getting denser: more cores and threads, more GPU cards, more memory. Applications do not necessarily scale even within a node. The deck names shared memory here: OpenMP, MPI shared memory, and pthreads.

## One job per command

Sam's thousand short commands, each with its own `sbatch`, give the scheduler a thousand jobs. Each job waits for an allocation, writes a job record, and starts a shell. The commands themselves are the small part.

The allocation should start the next task when a core is free. The scheduler then sees one job. Something inside that job hands work to a free core.

![Many tasks inside one Slurm job. The nodes drawn are one allocation, one pilot, and many tasks. The arrows read "one Slurm job" and "starts the next free task".](fig/many-tasks.svg){alt='Many tasks inside one Slurm job. The nodes drawn are one allocation, one pilot, and many tasks.'}

## Tools on the deck

The deck lists three ways to do this.

- Linux background processes on one node, placed with `numactl`. Snellius supports that. It needs bash and care about where each process sits. Someone who knows the placement has full manual control.
- Slurm arrays, for similar jobs. Snellius supports them. They have limits. The next episode teaches the limits and the control variables.
- A service that runs many jobs inside one allocation. QCG-PilotJob is the service this course walks through. It needs Python. The documentation is <https://qcg-pilotjob.readthedocs.io/en/develop/>.

The last episode compares four tools on the same two exercises: QCG-PilotJob, HyperQueue, Snakemake, and FireWorks. That comparison has a measured table. This episode does not. The discussion is the cost of a thousand separate jobs, and the shape of an allocation that refills a free core.

::: discussion

## Where the time goes

Take a command that runs for about a second. You submit it with its own `sbatch`, a thousand times.

Where does the time go, beyond that one second? When the work sits inside one allocation, what should happen at the moment a core becomes free?

:::

::: keypoints

- Many independent tasks on a dense node are the embarrassingly parallel case.
- A thousand one-task jobs spend their time in the scheduler.
- The allocation should start the next task when a core is free.
- Arrays come next. QCG-PilotJob is the pilot service. HyperQueue, Snakemake, and FireWorks are the other three tools in the last episode.

:::
