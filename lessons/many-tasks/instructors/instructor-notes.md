---
title: Instructor notes
---

## Timing

| Episode | Teaching | Exercises |
| --- | --- | --- |
| Embarrassingly parallel | 15 | 0 |
| Slurm arrays | 15 | 25 |
| QCG-PilotJob | 25 | 20 |
| Averages with a dependency | 10 | 25 |
| Idle time | 10 | 20 |
| Other tools (optional) | 20 | 25 |

The last episode is optional. Keep FireWorks in it when you teach it. The first episode is a discussion. The measured table stays in the last episode.

## Decks

QCG slides and examples 01 to 05: branch `fix/slides-qcg-source`, commit `cc9675bb69b01d8b339808d6715d52cbdeb5afde`.

Workflow slides and `alternatives/`: branch `feat/workflow-alternatives`, commit `6cada3eb5c7ae5e9fbed91d91ce27a34b0ae4b93`.

`PROVENANCE.md` records both pairs. The hands-on tree is `episodes/files/hands-on/`. Leave the directory layout alone. `alternatives/hyperqueue/average.sh` extracts `../../example_04/input.tar.gz`.

## Prep

`input.tar.gz` is already in `example_02` and `example_04`. `prepare_input.sh` builds `input_mod/`. Example 4 extracts with `tar -xvf input.tar.gz`.

Published scripts request the `rome` partition and, for example 3, 128 tasks per node. Leave those lines. Overrides go on the `sbatch` command. The hands-on README's small-node forms are `--array=0-99%10`, `QCG_MAX_INPUTS=100` with `--ntasks=2`, and `TIMES_FILE=times_short.txt` with `--ntasks=2`. Example 3's README example is `sbatch --nodes=3 --ntasks-per-node=2 qcg_job.sh`. Check `sinfo` before you quote a core count. The course cluster is a SURF Research Cloud workspace. The course tab requests `--partition=rome`. The cpu-minimum tab is the two-core override when `sinfo` shows small nodes.

QCG in the published scripts is `source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module use /cvmfs/course.surf-src.cvmfs/eessi/versions/2025.06/software/linux/x86_64/amd/zen2/modules/all` and `module load QCG-PilotJob/0.14.1-GCCcore-14.2.0`. The 2025 stack has no build of it. EESSI 2025.06 does not include it. The qcg-modules tab is the load line for the room. `episodes/files/exercises/qcg-three.py` prints `qcg-finished` and then `task-0`. That prediction is the two `print` calls plus `out_0.txt`. It does not depend on a cluster hostname.

`qcg_job.sh` in example 4 calls `qcg_job_v1.py`. The other versions are comments. One active line at a time.

`times_short.txt` is the first 32 lines of `times.txt` (160 lines). Those 32 numbers sum to 338. The longest is 56 and the shortest is 2. Keep those lengths. The README says shorter sleeps make QCG's per-task start-up dominate, and the comparison turns around.

The 25 October 2026 table is one run on two-core nodes, 2 slots, FireWorks on its one worker. Say so before you read a percentage. `measurements/sacct.txt` is Slurm's Elapsed, AllocCPUS, state, and exit code for the nine job ids. The idle percentages use `START` and `END` inside the output files. Those two clocks differ on the profile jobs. Job `16235860` in the example 4 README is a different example (16 CPUs, `CPUTimeRAW` 7232, 2.0 SBU). It is not one of the nine lines.

`example_01/array_job.sh` has a non-breaking space in three echo strings, before `$SLURM_ARRAY_TASK_ID`, `$SLURM_ARRAY_TASK_MAX`, and `$SLURM_ARRAY_TASK_MIN`. The variables still expand. Leave the file.

The v0 comment says "CVS". The inputs are CSV.

## Common mistakes

- One `sbatch` per short command. The first episode is about that cost. It is a discussion. There is no timing table in it.
- Editing `#SBATCH` inside the published script. Pass `--array`, `--ntasks`, or `--ntasks-per-node` on the command line.
- Submitting example 2 as `--array=0-999` on a two-core node. Use `--array=0-99%10`.
- Reading example 1's hostnames as if they must all differ. `TMPDIR` differs because each array element has its own node-local directory. Hostnames differ when the nodes differ.
- Running two versions at once in `qcg_job.sh`.
- Treating v0's `result.csv` as a finished aggregate. v0 has no `after`. v1 is the first file with `after=job_names`.
- Replacing `times_short.txt` with smaller integers.
- Starting a second `rlaunch` worker on the file LaunchPad. States get lost and the aggregate never runs. FireWorks in this tree is one worker and `--ntasks=1`.
- Ranking the tools from the 25 October table as if it were general. The slide says it is one run.
- Equating a span such as 267 s with the Elapsed field `00:04:35` on job 18158.
