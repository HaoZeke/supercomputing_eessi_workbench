---
title: "One request"
---

By the end of the Slurm episode you should be able to write one request without looking it up. It names the job, the partition, the cores, the time, and the output file. Then it loads the stack and runs one program.

## On the course cluster

``` {.bash org-language="sh"}
#!/bin/bash
#SBATCH --job-name=pi-one
#SBATCH --partition=thin_course
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --output=pi-%j.out

module purge
module load 2025
export SAMPLE_COUNT=1000
python3 pi_one.py
```

`rome` and `thin_course` are the same CPU nodes on this cluster. One core is the right request for this program. The file in the lesson is `episodes/files/pi-course.sh`.

## On Snellius

``` {.bash org-language="sh"}
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

A smaller core count on `rome` is rounded up to 16. Ask for 16 so the script matches the charge. The file in the lesson is `episodes/files/pi-snellius.sh`.

## What you submit

From the directory that contains `pi_one.py`:

``` {.bash org-language="sh"}
sbatch pi-course.sh
squeue -u "$USER"
```

One submission. If the state is `PD`, the job is waiting. Submit it again and you have two jobs. `scancel` plus the job id removes one you do not want.

The array form, when you want four sample sizes from one script, is `episodes/files/pi-array.sh`. `SLURM_ARRAY_TASK_ID` picks the size. That is the second request, not a replacement for being able to write the first one.
