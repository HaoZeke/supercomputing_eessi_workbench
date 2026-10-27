---
title: "Slurm arrays"
teaching: 15
exercises: 25
---

::: questions

- What is the same across every task in a Slurm array, and what can change?
- How do you cap how many tasks run at once, and how does each task find its index?

:::

::: objectives

- List the deck's limits: same options, Snellius max array size 30000, Snellius minimum 16 cores and 28 GiB on `rome`, and a wait for every task.
- Use `SLURM_ARRAY_TASK_ID`, the `%` throttle, and `%A` / `%a` in output names.
- Run example 01 and explain why each element has its own `$TMPDIR`.
- Run example 02, aggregate to `result.csv`, and scale with `--array=0-99%10` on 2 cores.

:::

## Collections of similar jobs

A Slurm job array submits and manages a collection of similar jobs. Every task has the same initial options: the same size, the same time limit, and the same script. The index is what changes.

The deck's limits:

- The maximum array size depends on the Slurm configuration. On Snellius it is 30000.
- The allocation for each task cannot be smaller than the site's minimum. On Snellius that minimum is 16 cores and 28 GiB of memory on the `rome` partition.
- You wait for each task to be allocated, and you wait for each task to finish. A short task does not hand its cores to the next index. The next index is another Slurm task.

This is the shape the deck shows. `sbatch --array=0-10 job.sh` creates 11 tasks, indexes 0 through 10.

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 2
#SBATCH -p rome
#SBATCH -t 1
hostname
```

`-t 1` is one minute. `-n 2` is two tasks. At one core per task that is two cores, under the 16-core minimum the deck states for Snellius on `rome`. The slide uses the small request to show the array syntax. The minimum still applies on Snellius.

The published scripts in the hands-on keep their own `#SBATCH` lines, including `-p rome`. The tab is the request for the machine in your welcome note.

## Ways of control

Each task sees `SLURM_ARRAY_TASK_ID` set to its index.

A `%` in the array range caps how many tasks run at once.

```bash
sbatch --array=0-10 job.sh
sbatch --array=0-10%2 job.sh
```

The first line creates 11 tasks. The second tells Slurm to run at most 2 of them at the same time. The command still returns one array job id.

The deck's control script prints the index and the hostname:

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 2
#SBATCH -p rome
#SBATCH -t 1
echo "SLURM_ARRAY_TASK_ID: $SLURM_ARRAY_TASK_ID"
hostname
```

Five variables are worth learning as a set.

| Variable | What it holds |
| --- | --- |
| `SLURM_ARRAY_JOB_ID` | The first job ID of the array |
| `SLURM_ARRAY_TASK_ID` | This task's index |
| `SLURM_ARRAY_TASK_COUNT` | How many tasks the array contains |
| `SLURM_ARRAY_TASK_MAX` | The highest index |
| `SLURM_ARRAY_TASK_MIN` | The lowest index |

Output names can use two replacements. `%A` becomes `SLURM_ARRAY_JOB_ID`. `%a` becomes `SLURM_ARRAY_TASK_ID`.

```bash
#SBATCH --output slurm-%A_%a.out
```

:::: challenge

## Count and cap

`sbatch --array=0-10 job.sh` and `sbatch --array=0-10%2 job.sh` are the deck's pair. How many tasks does the first create? How many run at once in the second?

::: solution

## Solution

`--array=0-10` creates 11 tasks, because the indexes run from 0 through 10. `--array=0-10%2` is the same 11 tasks, and Slurm runs at most 2 of them at the same time.

:::

::::

## Example 1: hostname and TMPDIR

`episodes/files/hands-on/example_01/array_job.sh` submits 12 tasks, indexes 0 through 11, at most 3 at once. Each task is 1 node and 1 task, partition `rome`, ten minutes (`-t 10`).

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -p rome
#SBATCH -t 10
#SBATCH --array 0-11%3

echo "Running on "
hostname
echo "TMPDIR $TMPDIR"

echo "SLURM_ARRAY_JOB_ID $SLURM_ARRAY_JOB_ID"
echo "SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_ID"
echo "SLURM_ARRAY_TASK_COUNT $SLURM_ARRAY_TASK_COUNT"
echo "SLURM_ARRAY_TASK_MAX $SLURM_ARRAY_TASK_MAX"
echo "SLURM_ARRAY_TASK_MIN $SLURM_ARRAY_TASK_MIN"
```

The file in the tree has a non-breaking space in three of those echo strings. The variables are the same five from the table.

Each array element is its own job, so each element has its own node-local directory. The `TMPDIR` lines differ for that reason. Hostnames differ when two elements run on different nodes. They can repeat when two elements share a node. The directory still differs, because the path is per job.

`$TMPDIR` on your machine:

::: sites tmpdir
:::

:::::::::::: challenge

## Why the directories differ

Example 1 prints `hostname` and `TMPDIR` twelve times. Which of those two values is a new path for every element, and why?

::: sites tmpdir
:::

::: solution

## Solution

`TMPDIR` is a new path for every element. Each array task is its own job, and the job's node-local directory is removed when that task ends. The tab says where that directory lives on this machine.

Hostnames match when two tasks share a node, and they differ when Slurm places the tasks on different nodes. Twelve output files is the count of indexes 0 through 11. `%3` caps the running set at 3. It does not change the count.

:::

::::::::::::

## Example 2: one column, then result.csv

Example 2 averages one column of each CSV and gathers the averages into `result.csv`. The files are the NOAA Global Historical Climatology Network daily set: <https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily>.

From `episodes/files/hands-on/example_02`:

```bash
./prepare_input.sh
sbatch array_job.sh
./aggregate.sh <job_id>
```

`prepare_input.sh` extracts `input.tar.gz` and copies each file from `input/` into `input_mod/` with a numeric prefix, starting at 0. The array script selects `input_mod/${SLURM_ARRAY_TASK_ID}_*`.

The published header is 1000 tasks, indexes 0 through 999, at most 10 at once, one task each, partition `rome`, ten minutes:

```bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -p rome
#SBATCH -t 10
#SBATCH --array 0-999%10
```

Inside the task the script loads `module load 2025` and `module load Python/3.13.1-GCCcore-14.2.0`, copies `input_mod` and `average.py` into `$TMPDIR`, and runs `python3 average.py` on that one file. `average.py` prints one line, `dataset_name,mean`.

`aggregate.sh` takes the job id `sbatch` printed. It reads `slurm-<job id>_*.out`, keeps the average line, and sorts them into `result.csv`. The deck's `--output slurm-%A_%a.out` is the same shape of name. The result of the exercise is `result.csv`.

The deck asks for the total execution time and the system billing units. `sacct` is the tool. Example 4's README works one job in full (job `16235860`, `CPUTimeRAW` 7232, 2.0 SBU). Use that conversion when you have a `CPUTimeRAW` column. On a machine that does not bill in system billing units, that column is still core-seconds, and core-hours are `CPUTimeRAW / 3600`.

On 2 cores the hands-on README runs 100 of the 1000 files:

```bash
sbatch --array=0-99%10 array_job.sh
```

Leave the script's `--array 0-999%10` line as published. The smaller range is an override on the command line.

::: sites scale-two-core
:::

## QCG is next

This episode stops at arrays. You still wait for each task to be allocated and to finish. The next episode is QCG-PilotJob, which keeps one allocation and starts the next task itself. The load line for that tool:

::: sites qcg-modules
:::

:::::::::::: challenge

## A hundred files on two cores

You are in `example_02`. `prepare_input.sh` has already built `input_mod/`. The node has two cores. What do you pass to `sbatch`, and what file do you have after `aggregate.sh`?

::: sites scale-two-core
:::

::: solution

## Solution

```bash
sbatch --array=0-99%10 array_job.sh
./aggregate.sh <job_id>
```

The override selects indexes 0 through 99, at most 10 at once, which is 100 of the 1000 files. The script in the tree still says `0-999%10`. After every selected task has finished, `aggregate.sh` writes `result.csv`.

:::

::::::::::::

::: keypoints

- An array is a collection of similar jobs. Every task shares the initial options.
- On Snellius the deck's maximum array size is 30000, and the minimum allocation on `rome` is 16 cores and 28 GiB.
- `--array=0-10` is 11 tasks. `--array=0-10%2` runs at most 2 at once.
- `SLURM_ARRAY_TASK_ID` is the index. `%A` and `%a` fill in the job id and the index in a file name.
- Example 1's `$TMPDIR` values differ because each element has its own node-local directory.
- Example 2's aggregate writes `result.csv`. On 2 cores: `sbatch --array=0-99%10 array_job.sh`.

:::
