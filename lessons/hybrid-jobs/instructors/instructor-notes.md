---
title: Instructor notes
---

## Timing

| Episode | Teaching | Exercises |
| --- | --- | --- |
| Nodes, tasks, and threads | 20 | 20 |
| AXPY | 15 | 25 |
| Dot product | 15 | 25 |
| Matrix multiplication | 10 | 30 |

## License

The TODO(Rohit) callout at the top of the lesson is still open. Keep the names: José Luis Bosque, Borja Pérez, Ramón Beivide, and Carmen Martínez, Universidad de Cantabria, EuroCC NL at SURF. Leave that callout in place for the whole class.

## Cluster tabs

The course cluster is a SURF Research Cloud workspace. The course tab requests `--partition=rome`. Snellius keeps the `#SBATCH` lines in the scripts. The course tab of the two-core snippet has the override table. Command-line `sbatch` options override those lines. Learners should not edit the scripts to shrink a job.

The sample output times in the episodes are one recorded run from the module. Learners record their own times. AXPY is limited by memory bandwidth, so those times flatten early. Teach that shape. The seconds come from the room's jobs.

## Idris

Idris requests one core and 16 threads. `--cpus-per-task` is the core count. The hybrid scripts set the thread count from that variable. One core runs one thread at a time. Sixteen threads need sixteen cores on a machine that has them.

## Network

Snellius uses InfiniBand. The course machines use Ethernet. Cross-node scaling on the course machines is weaker. Say that before anyone compares a three-node course run with a Snellius run.
