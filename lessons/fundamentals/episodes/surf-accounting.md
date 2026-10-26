---
title: "Accounting on Snellius"
teaching: 20
exercises: 10
---

::: questions
- What is a system billing unit, and which row of the table sets the price?
- How many SBU does 16 cores for 2 hours cost on `rome`?
- What does the course cluster charge instead?
:::

::: objectives
- Read the Snellius system-details table: nodes, cores, memory, SBU per hour, smallest allocation.
- Compute an SBU cost from cores, hours, and the SBU rate of the partition.
- Say what a full CPU allocation does to idle GPUs, and what a one-core request is rounded up to.
:::

## The table you are billed from

Snellius charges system billing units (SBU). The accounting portal is <https://portal.cua.surf.nl/>.

A `rome` node is the row most jobs in this course start from: 521 nodes, 128 cores, 256 GB, AMD Rome 7H12 at 2.6 GHz, 128 SBU per node-hour. The smallest allocation is 1/8 of a node, which is 16 cores.

The same table has more partitions. GPU counts are per node. `gpu_a100` is 4 NVIDIA A100 40 GB. `gpu_h100` is 4 NVIDIA H100 (SXM5) 94 GB.

| Partition | Nodes | Cores | Memory | SBU/hour | Smallest |
| --- | --- | --- | --- | --- | --- |
| rome | 521 | 128 | 256 GB | 128 | 1/8 |
| fat_rome | 72 | 128 | 1,024 GB | 192 | 1/8 |
| himem_4tb | 2 | 128 | 4,096 GB | 256 | 1/8 |
| himem_8tb | 2 | 128 | 8,192 GB | 384 | 1/8 |
| genoa | 737 | 192 | 384 GB | 192 | 1/8 |
| fat_genoa | 48 | 192 | 1,536 GB | 288 | 1/8 |
| gpu_a100 | 63 | 72 | 512 GB | 512 | 1/4 |
| gpu_h100 | 88 | 64 | 768 GB | 768 | 1/4 |
| staging | 10 | 16 | 256 GB | 32 | 1/32 |

Login nodes are a separate row of 3 machines. Do not run a heavy task there. Their hardware is not one of the rows above.

The whole machine in the deck's summary line is 1,258 thin rome/genoa nodes, plus the fat and high-memory nodes, plus 604 GPUs. Home is 720 TB. Scratch and project together are 12.4 PB, on GPFS.

## The formula

Documentation talks about cores. The charge uses the partition's SBU per node-hour and the number of cores on that node:

```text
cores x hours x (SBU per node-hour / cores per node)
```

16 cores for 2 hours on `rome`:

```text
16 x 2 x (128 / 128) = 32
```

16 cores is 1/8 of 128, so it is the smallest `rome` job. At 128 SBU per node-hour that slice is 16 SBU per hour. Two hours is 32 SBU.

A full `rome` node for one hour is 128 cores, which is 128 SBU. Asking for fewer cores than the smallest unit does not make a cheaper job. The system rounds the request up to that unit, and the job gets every core in the unit.

## The tightest resource wins

Each node has cores, memory, accelerators, and local disk. The allocation follows the most restrictive thing you asked for.

If you request every CPU core and no GPU, the node is fully allocated. The GPUs sit idle, and nobody else can use them, because the CPUs are taken.

If you request one core, the system rounds up to the smallest permitted unit. On `rome` that unit is 1/8 of the node. You then have every core in that unit, not the single core you typed.

:::::: group-tab

### Snellius

The `rome` row of the accounting table is 521 nodes, 128 cores, 256 GB, 128 SBU per hour, smallest allocation 1/8 of a node.

16 cores is 1/8 of 128, so it is the smallest `rome` job. At 128 SBU per node-hour that is 16 SBU per hour. Two hours is 32 SBU.

```text
cores x hours x (SBU per node-hour / cores per node)
16 x 2 x (128 / 128) = 32
```

### Course cluster

There is no project budget and `accinfo` is not installed. `sacct` still reports core-seconds in `CPUTimeRAW`.

```bash
sacct -j JOBID --format=JobID,Elapsed,AllocCPUS,CPUTimeRAW
```

### Magic Castle

```bash
sacct -j JOBID --format=JobID,Elapsed,AllocCPUS,TotalCPU
```

There is no SURF system billing unit on this cluster.

::::::

Read the tab for the machine in the welcome note. The Snellius tab is the SBU table above. The course-cluster tab has no project budget.

:::::: group-tab

### Snellius

Snellius is the Dutch national supercomputer, operated by SURF. Login nodes are named `int*`. A compute node name looks like `tcn386`. The public description is at <https://www.surf.nl/en/services/compute/snellius-the-national-supercomputer>.

### Course cluster

::: callout
## TODO(Rohit)

The course cluster name and partition for the next run are still open.
The workbench uses a Magic Castle workspace and `--partition=thin_course`.
The course README says SURF Research Cloud workspaces and the partition `rome`.
The fundamentals deck says those two partition names point at the same nodes.
This tab does not choose.
:::

Use the address in the welcome note. There is one login node. `module load 2025` loads EESSI 2025.06. There is no project budget. `sacct` still reports core-seconds in `CPUTimeRAW`.

### Magic Castle

This tab is the HPC Carpentry cloud cluster: Magic Castle with the EESSI software stack. Accounts are requested at <https://cluster.hpc-carpentry.org>. The login host is `cluster.hpc-carpentry.org`.

::::::

:::::::::::: challenge
## Cost a rome job

A job asks for 16 cores on `rome` and runs for 2 hours. How many SBU is that? Why is 16 the interesting number, rather than 8?

:::::: solution
## Solution

32 SBU.

```text
16 x 2 x (128 / 128) = 32
```

16 cores is 1/8 of a 128-core `rome` node, and 1/8 is the smallest allocation on that row. A request for 8 cores is rounded up to that same unit, so it does not cost half as much.
::::::
::::::::::::

:::::::::::: challenge
## Cost a genoa slice

`genoa` is 192 cores and 192 SBU per node-hour. The smallest allocation is still 1/8 of a node. A job uses 24 cores for 1 hour. How many SBU?

:::::: solution
## Solution

24 SBU.

```text
24 x 1 x (192 / 192) = 24
```

24 cores is 192/8, so this is one smallest unit for one hour. One full `genoa` node-hour is 192 SBU.
::::::
::::::::::::
