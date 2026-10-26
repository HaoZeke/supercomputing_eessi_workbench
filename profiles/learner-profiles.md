---
title: "Learner profiles"
---

Three people this day is for. The exercises assume a terminal and a text editor. They do not assume a previous batch job.

## Noor, first year, laptop only

Noor writes Python on a laptop and has just been told the data set is on Snellius. Noor can use a terminal and has not seen a module or a queue. Noor needs episode 1 and episode 2 before any of the later material makes sense. The win for Noor is a single `sbatch` that runs `pi_one.py` and a clear rule about which directory holds the result.

## Idris, SSH works, jobs do not

Idris has logged in before and has a directory of scripts in `/home`. Jobs sit in the queue, or they die at the start because the module was loaded in a different order last time. Idris needs the header in the Slurm episode, `module purge` before `module load`, and the filesystem table. The array is the part Idris came to see.

## Sam, a thousand short commands

Sam already submits jobs and is now generating thousands of one-second tasks. The queue time is longer than the work. Sam can skim episodes 1 and 2, should still do the filesystem episode because the outputs are many small files, and should spend the afternoon on QCG-PilotJob and the one-page comparison with HyperQueue, Snakemake, and FireWorks. The timing episode is there so Sam can say whether more cores helped, with a number.

## What you do not need

You do not need to compile a program, write a workflow engine, or read an EasyBuild recipe. Those are real skills, and they are the book at <https://hpceb.rgoswami.me/>, not this day.
