# Commands for the course cluster

Open VS Code from Open OnDemand, choose **1 core**, and use its Terminal menu for these commands. The browser Shell works too. Keep the exercise page open for explanations. Copy one block at a time; replace JOBID with the job number Slurm prints.

The cluster has three 2-CPU nodes and one 60-CPU GPU node: 66 schedulable CPUs in total. The GPU node has two RTX PRO 6000 Blackwell cards. Partitions share these nodes; their totals must not be added together. CPU requests below use at most two cores for the small-node exercises. No email notifications are configured.

## 1. Find your account and the prepared exercises

```bash
whoami
hostname
pwd
sinfo
cd "$HOME/introduction-to-supercomputing/course-module-fundamentals-of-hpc/hands-on"
ls
```

The exercises are prepared in the Introduction attendees' homes. For a separate copy, use the [classroom fork](https://github.com/HaoZeke/introduction-to-supercomputing/tree/course/maastricht-20261028). Keep any existing work.

```bash
git clone --branch course/maastricht-20261028 --single-branch \
  https://github.com/HaoZeke/introduction-to-supercomputing.git \
  "$HOME/introduction-to-supercomputing-class"
```

## 2. Select software and submit Python

Run from the fundamentals hands-on directory. The script selects its own Python module inside the job.

```bash
module load 2025
module list
sbatch --partition=rome --cpus-per-task=1 python.sh
squeue --me
```

Replace JOBID below. Expect a compute hostname and `sum: 499999500000`.

```bash
cat slurm-JOBID.out
seff JOBID
sacct -j JOBID --format=JobID,JobName,State,ExitCode,Elapsed,AllocCPUS
```

[Open python.sh](https://github.com/HaoZeke/introduction-to-supercomputing/blob/course/maastricht-20261028/course-module-fundamentals-of-hpc/hands-on/python.sh).

## 3. Compile and run the OpenMP pi example

The small-node request below overrides the script's 32-core default. The script runs its thread counts only up to the allocation size.

```bash
./compilepi
sbatch --partition=rome --cpus-per-task=2 pi.sh
squeue --me
```

[Open pi.sh](https://github.com/HaoZeke/introduction-to-supercomputing/blob/course/maastricht-20261028/course-module-fundamentals-of-hpc/hands-on/pi.sh) and [pi.c](https://github.com/HaoZeke/introduction-to-supercomputing/blob/course/maastricht-20261028/course-module-fundamentals-of-hpc/hands-on/pi.c).

## 4. Filesystems

Home and scratch are shared filesystems. `~/scratch` points to your scratch directory. `myquota` reports the filesystem that contains your home; its BeeGFS capacity display describes shared space, not your personal usage.

```bash
printf 'Home: %s\nScratch: /scratch/%s\n' "$HOME" "$USER"
df -h "$HOME" "/scratch/$USER"
myquota
ls -ld "$HOME/scratch" /project/learners
```

`$TMPDIR` exists inside a Slurm job. On this cluster, omit the Snellius-only `--constraint=scratch-node` option.

```bash
srun --partition=rome --nodes=1 --ntasks=1 --cpus-per-task=1 --time=00:02:00 \
  bash -c 'hostname; printf "Job scratch: %s\n" "$TMPDIR"; test -d "$TMPDIR"'
```

[Filesystem exercises](https://github.com/HaoZeke/introduction-to-supercomputing/tree/course/maastricht-20261028/course-module-snellius-fs).

## 5. QCG-PilotJob

The real course installation is in the course CernVM-FS repository. These initialization commands belong inside a job script when the job uses QCG-PilotJob.

```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module use /cvmfs/course.surf-src.cvmfs/eessi/versions/2025.06/software/linux/x86_64/amd/zen2/modules/all
module load QCG-PilotJob/0.14.1-GCCcore-14.2.0
```

Example 4 uses the prepared input archive. Limit it to 100 inputs and two slots for the teaching exercise.

```bash
cd "$HOME/introduction-to-supercomputing/course-module-qcg-pilotjob/hands-on/example_04"
QCG_MAX_INPUTS=100 sbatch --partition=rome --ntasks=2 qcg_job.sh
```

Example 5 compares 32 tasks at their original durations. Submit each job once and keep the printed job numbers.

```bash
cd "$HOME/introduction-to-supercomputing/course-module-qcg-pilotjob/hands-on/example_05"
TIMES_FILE=times_short.txt sbatch --partition=rome --ntasks=2 qcg_job.sh
TIMES_FILE=times_short.txt sbatch --partition=rome --ntasks=2 pipeline.sh
```

[All QCG exercise scripts and inputs](https://github.com/HaoZeke/introduction-to-supercomputing/tree/course/maastricht-20261028/course-module-qcg-pilotjob/hands-on).

## 6. HyperQueue and workflow alternatives

Use the same EESSI initialization and course module directory as above, then select the real HyperQueue module.

```bash
module load HyperQueue/0.24.0
```

```bash
cd "$HOME/introduction-to-supercomputing/course-module-qcg-pilotjob/hands-on/alternatives/hyperqueue"
QCG_MAX_INPUTS=100 sbatch --partition=rome --ntasks=2 average.sh
TIMES_FILE=times_short.txt sbatch --partition=rome --ntasks=2 profile.sh
```

[HyperQueue, Snakemake and FireWorks scripts](https://github.com/HaoZeke/introduction-to-supercomputing/tree/course/maastricht-20261028/course-module-qcg-pilotjob/hands-on/alternatives). Follow each tool's initialization instructions; the FireWorks example needs its configured database and worker.

## 7. Hybrid jobs, performance and moving data

These are optional previews in the four-hour route. Use the complete exercise instructions, including the two-core SRC overrides, before submitting a job.

- [Hybrid MPI and OpenMP exercises](https://github.com/HaoZeke/introduction-to-supercomputing/tree/course/maastricht-20261028/course-module-snellius-hybrid-jobs/hands-on)
- [Performance examples](/commands/performance.html)
- [Moving data examples](/commands/data-movement.html)
- [Filesystem examples](/commands/filesystems.html)

## 8. Stop your editor when finished

Stop VS Code under **My Interactive Sessions** in Open OnDemand. Closing its browser tab leaves the Slurm job running. You can see both editor sessions and submitted exercise jobs here:

```bash
squeue --me
```

Keep the job IDs you need for `seff` and `sacct`. Saved files stay in your home when the editor session ends.
