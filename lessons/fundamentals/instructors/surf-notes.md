---
title: "Instructor notes"
---

## Timing

The hpc-intro episodes keep their upstream times. The last two episodes are from the SURF fundamentals deck.

| Episode | Teaching | Exercises |
| --- | --- | --- |
| Why use a Cluster? | 15 | 5 |
| Connecting to the remote cluster | 35 | 0 |
| Exploring the cluster | 25 | 10 |
| Scheduling jobs | 45 | 30 |
| Environment variables | 10 | 5 |
| Software modules | 30 | 15 |
| Transferring files | 15 | 15 |
| Running a parallel job | 30 | 60 |
| Job arrays | 15 | 5 |
| Using resources effectively | 10 | 20 |
| Your responsibilities as an HPC user | 15 | 5 |
| Accounting on Snellius | 20 | 10 |
| Python and OpenMP on a node | 10 | 25 |

If the room is short on time, keep the 32 SBU example and one `pi = 3.141592654` line. The genoa cost can go. On a two-core node, submit `sbatch --cpus-per-task=2 pi.sh` and do not edit the script.

## Source

Accounting numbers are the system-details table in `course-module-fundamentals-of-hpc/slides/fundamentals-of-hpc.org`.

The Python and OpenMP scripts are `course-module-fundamentals-of-hpc/hands-on/`.

Branch: `fix/slides-fundamentals-source`

Commit: `2ebb95294418d5831143e393e93b294af39464b1`

The course-cluster note is the slide "This course runs on a course cluster built like Snellius". The course tab still has TODO(Rohit). Do not pick `thin_course` or `rome` for that tab. The published scripts keep `--partition=rome`.

## Upstream

The rest of the lesson is hpc-intro at `7081080674aceeb0a4bc57b9348da22d876af802`, CC-BY 4.0, Carpentries authors in `AUTHORS`. See `UPSTREAM.md`.
