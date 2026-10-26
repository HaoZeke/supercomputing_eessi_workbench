---
title: "Instructor notes"
---

## Timing

| Episode | Teaching | Exercises |
| --- | --- | --- |
| A shared software stack | 15 | 10 |
| Finding and loading a module | 20 | 20 |
| The EESSI client container | 15 | 15 |

Teaching is 50 minutes and exercises are 45 minutes. If the room is short on time, keep the CPU-line challenge and the `Python 3.13.5` check. Skip the 2023.06 load.

## Source

The environment-modules section of the deck, from the heading "Environment modules" through the Lmod command table, is `course-module-fundamentals-of-hpc/slides/fundamentals-of-hpc.org` in <https://github.com/HaoZeke/introduction-to-supercomputing>.

Branch: `fix/slides-fundamentals-source`

Commit: `2ebb95294418d5831143e393e93b294af39464b1`

The course-cluster note on that deck is the slide "This course runs on a course cluster built like Snellius". The version strings `Python/3.13.5-GCCcore-14.3.0` and `Python/3.11.5-GCCcore-13.2.0`, the init-script transcript, and the two `EESSI_*` variables are from the software episode this lesson replaces. They are not printed on that slide.

EasyBuild stays a pointer. Book: <https://hpceb.rgoswami.me/>. Sources: <https://github.com/HaoZeke/what-easybuild-is-doing>.

## What to skip

Do not open EasyBuild. Do not search the EESSI tree for `QCG-PilotJob`. Do not download the client image if everyone already has a cluster login. The container episode is then a reading of the two variables and the CPU line.

## Common mistakes

- `module load` of a second stack in a shell that already has one. `module purge` comes first.
- Copying a neighbour's CPU directory into a script. The init script picks the path.
- `module spider QCG-PilotJob` in the container, then a private install. The tool is a site module. The tab has the load line.
- A long Python script on the login node. `python3 --version` is the command that belongs there.
- `module load 2025` and a second `source` of the init script in the same shell.
- Expecting `sbatch` inside the client container.

## Prep checklist

- [ ] Confirm which machine the room will use. The tabs differ.
- [ ] On a cluster, from a clean shell, `module load 2025` then `module load Python/3.13.5-GCCcore-14.3.0`, and `python3 --version` prints `Python 3.13.5`.
- [ ] `module spider QCG-PilotJob` does not find it in a pure EESSI shell. After the site load in the QCG tab, `module list` shows `QCG-PilotJob`.
- [ ] If you will teach the container live, pull `docker://ghcr.io/eessi/client:rocky8` once before the room arrives. Apptainer must be 1.0 or newer and must support `--fusemount`.
- [ ] Decide whether the 2023.06 purge-and-load is in the exercise or only on the board. It needs a shell you can purge.

## What to collect

One `python3 --version` line that reads `Python 3.13.5`, and one CPU line from the init script. The CPU name will differ between laptops. That difference is the point.
