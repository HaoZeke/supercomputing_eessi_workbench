---
title: "Submitting a job"
teaching: 35
exercises: 25
---

::: questions
- How do you ask Slurm for time and cores without starting the work on the login node?
- What does a job array change, compared with four separate scripts?
:::

::: objectives
- Write a batch script with a job name, a partition, a core count, a time limit, and an output file.
- Explain why Snellius rounds a small request up to 16 cores on the `rome` partition.
- Submit a script with `sbatch` and read its state with `squeue`.
- Use `SLURM_ARRAY_TASK_ID` to give each array task a different input.
- Cancel a job you submitted by mistake with `scancel`.
:::

## The script is the request

A batch script is a shell script with a header of `#SBATCH` lines. Slurm reads the header. The shell runs the rest, on a compute node, after the wait.

This is the Snellius shape. The file in the lesson is `episodes/files/pi-snellius.sh`.

``` bash
#!/bin/bash
#SBATCH --job-name=pi-one
#SBATCH --partition=rome
#SBATCH --cpus-per-task=16
#SBATCH --time=00:15:00
#SBATCH --output=pi-%j.out

module purge
module load 2025
export SAMPLE_COUNT=1000
python3 pi_one.py
```

`%j` in the output name becomes the job id. `pi_one.py` prints one line, `samples=1000 hits`... estimate=...=. It uses a fixed random sequence, so the same `SAMPLE_COUNT` always prints the same line. The program is in `episodes/files/pi_one.py`.

On Snellius the `rome` partition gives memory with the cores, and the smallest slice is 16 cores. A request for 1 core is rounded up to 16, and the project is charged for 16. Asking for 16 in the script matches what you will be charged.

On the course cluster the same nodes answer to `rome` and to `thin_course`, and a node has two cores. Ask for one core there. `episodes/files/pi-course.sh` is that script: `--partition=thin_course` and `--cpus-per-task=1`.

Submit from the directory that contains `pi_one.py`:

``` bash
sbatch pi-course.sh
squeue -u "$USER"
```

`sbatch` prints `Submitted batch job` and a number. `squeue` shows `PD` while the job waits and `R` while it runs. When it leaves the queue, read `pi-<jobid>.out`.

::: callout
`srun` can start a step inside a job, or a short interactive allocation. `sbatch` is the command for a script you can resubmit. This lesson uses `sbatch`.
:::

The directives you will see most often are in `episodes/files/slurm-directives.tsv`. The same rows are below.

::: siteonly
<div class="table-responsive">

| directive | meaning | example | where |
|----|----|----|----|
| --job-name | a short name in the queue | pi-one | any Slurm cluster |
| --partition | which group of nodes | rome | Snellius and the course cluster |
| --cpus-per-task | cores for the one task | 16 | Snellius rome slice |
| --time | wall clock limit | 00:15:00 | any Slurm cluster |
| --output | file for the job text | pi-%j.out | any Slurm cluster |
| --array | one index per task | 0-3 | any Slurm cluster |

</div>
:::

## While you wait

A job in `PD` is waiting for resources. `squeue -u "$USER"` is enough during class. `scancel JOBID` removes a job you do not want. On Snellius, `scontrol show job JOBID` tells you why a job is still waiting. On the course cluster the reason is usually that someone else holds the two cores.

Do not resubmit because the first job is still `PD`. You will get two jobs, and then four.

## Four lengths, one script

A job array runs the same script many times. `SLURM_ARRAY_TASK_ID` is 0, 1, 2, or 3 when you ask for `--array=0-3`. `%A` is the array id and `%a` is the task id, so each task gets its own output file.

`episodes/files/pi-array.sh`:

``` bash
#!/bin/bash
#SBATCH --job-name=pi-array
#SBATCH --partition=thin_course
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --array=0-3
#SBATCH --output=pi-%A_%a.out

module purge
module load 2025
sizes=(1000 2000 4000 8000)
export SAMPLE_COUNT="${sizes[$SLURM_ARRAY_TASK_ID]}"
python3 pi_one.py
```

## A faded header

``` bash
#SBATCH --job-name=________
#SBATCH --partition=________
#SBATCH --cpus-per-task=________
#SBATCH --time=________
```

On the course cluster the partition is `thin_course` or `rome`, and the core count is `1` for this program. On Snellius `rome` the core count for this lesson is `16`.

:::: challenge
## Predict the array index

`sizes` has four numbers: 1000, 2000, 4000, 8000. The header says `--array=0-3`. Which `SAMPLE_COUNT` does task 2 export? Write the number before you look at the solution.

::: solution
## Solution

Task 2 exports 4000. The index starts at 0, so task 0 is 1000, task 1 is 2000, task 2 is 4000, and task 3 is 8000. The output file for task 2 is `pi-<arrayid>_2.out`.
:::
::::

:::: challenge
## Check the batch script

From the lesson directory:

``` bash
bash episodes/files/exercises/check-batch-script.sh
```

    batch-script=ok

Then, if you are on the course cluster, submit the one-core script and the array. Copy `pi_one.py` into the directory you submit from, or submit from `episodes/files`.

``` bash
cd episodes/files
sbatch pi-course.sh
sbatch pi-array.sh
squeue -u "$USER"
```

::: solution
## Solution

The check runs `bash -n` on `pi-snellius.sh` and requires the five directives plus `module load 2025`. A missing `--time` line makes it exit with an error.

After `sbatch`, `squeue` shows one job and an array. When they finish, `pi-<jobid>.out` contains one `samples=1000` line. The array writes four files. Task 0 prints `samples=1000`. You can also run `SAMPLE_COUNT=1000 python3 pi_one.py` on the login node for this tiny count if the queue is busy. 1000 samples is a login-node-sized test. The array sizes above 1000 belong in the job.
:::
::::

::: keypoints
- A batch script is a shell script plus `#SBATCH` resource lines.
- `sbatch` submits. `squeue` shows the wait. `scancel` removes a job.
- On Snellius `rome`, ask for 16 cores because smaller requests are rounded up.
- On the course cluster, ask for 1 core on `thin_course` or `rome`.
- `SLURM_ARRAY_TASK_ID` selects the input for one task in an array.
:::
