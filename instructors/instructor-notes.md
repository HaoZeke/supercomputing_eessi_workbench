---
title: "Instructor notes"
---

Teach this in one day next to the slide decks in <https://github.com/sara-nl/introduction-to-supercomputing>. Each episode below names the deck to have open. The episode slide deck in `slides/` is the backup if a course deck will not build.

## Timing

| Page                       | Teaching | Exercises |
|----------------------------|----------|-----------|
| what-is-a-supercomputer.md | 30       | 15        |
| software-with-eessi.md     | 30       | 20        |
| slurm-jobs.md              | 35       | 25        |
| filesystems-and-data.md    | 30       | 20        |
| many-tasks.md              | 30       | 20        |
| performance-first-steps.md | 25       | 20        |

Teaching is 180 minutes and exercises are 120 minutes. That is a full day with breaks, not six hours of talking. If you are short on time, keep the prediction in each episode and skip the second challenge.

## Deck map

- Episodes 1 and 2 follow `course-module-fundamentals-of-hpc/slides/fundamentals-of-hpc.pdf`. Stop the software episode at `module load`. Do not open EasyBuild. Point at <https://hpceb.rgoswami.me/> and move on.
- Episode 3 uses the scheduler section of that same fundamentals deck. The batch files in `episodes/files/` are the ones to project.
- Episode 4 follows `course-module-snellius-fs/slides/snellius-fs.pdf`. Draw `/home`, `/project`, and `/scratch` for the course cluster beside the Snellius table.
- Episode 5 follows `course-module-qcg-pilotjob/slides/qcg-pilotjob-slides.pdf` for the pilot, then `course-module-qcg-pilotjob/slides/workflow-alternatives.pdf` for HyperQueue, Snakemake, and FireWorks. Ten minutes on the alternatives is enough.
- Episode 6 follows `course-module-performance-analysis/performance-analysis.pdf`. Stop at the roofline picture. Do not start a profiler.

## Before the room arrives

Confirm which machine the room will actually use. Snellius and the course cluster do not share a host name. Put the course address on the board as `MANAGER` and leave `snellius.surf.nl` written next to it so the two ssh lines are not mixed up.

On the course cluster, check `module load 2024` and then `module load QCG-PilotJob` from a clean shell. If the site module is missing, teach the QCG section from the script and the figure, and do not ask the room to install a private copy.

If nobody has a cluster login, the EESSI client container covers episodes 2 and 6 and the pi program. It does not cover `sbatch`. Say that at the start.

## Common mistakes

- SSH to Snellius from a course-cluster shell, or the other way around.
- A long Python run on the login node. `SAMPLE_COUNT=1000` is the only size that belongs there.
- `module load` on top of another stack without `module purge`.
- Asking for 1 core on Snellius `rome` and then being surprised by a 16-core charge.
- A second `sbatch` while the first job is still `PD`.
- Copying a directory of tiny files with `rsync` and then blaming the network.
- `module spider QCG-PilotJob` inside the EESSI container. It is not there.
- Timing a larger `SAMPLE_COUNT` and calling the program slower.

## What to collect

One real job id from the room, one `pi-*.out` line, and the eight-core efficiency 0.625 from the table. Those three show that login, the queue, and the timing episode all happened.

## Building the lesson site

From a checkout, with pixi:

``` bash
pixi run build
pixi run gate
pixi run check
pixi run slides
pixi run site
```

`pixi run check` reruns the export, the offline exercises, the EESSI output blocks, and the slide build. The EESSI check needs the client image named by `EESSI_SIF`, or `/tmp/eessi-client.sif` if that variable is unset. A paragraph note from the prose gate does not fail the gate. A forbidden word, a dash, or a voice warning does.
