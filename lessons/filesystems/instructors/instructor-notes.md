---
title: "Instructor notes"
---

## Timing

| Episode | Teaching | Exercises |
| --- | --- | --- |
| Why I/O matters | 15 | 0 |
| The file systems | 20 | 10 |
| Files and directories | 10 | 25 |
| Permissions and quota | 10 | 20 |
| Space for a job | 15 | 25 |

Teaching is 70 minutes and exercises are 80 minutes. The first episode is a discussion, not a typing exercise. If the room is short on time, keep that discussion, the survival challenge, `chmod g-r`, and `iend=8 wdir=TMPDIR sbatch run.sh`. Skip scratch-node when the room is on the course cluster. Skip the optional thousand-file challenge whenever disk or time is tight.

## Source

The deck is `course-module-snellius-fs/slides/snellius-fs.org` in <https://github.com/HaoZeke/introduction-to-supercomputing>.

Branch: `fix/slides-fs-source`

Commit: `4709c85d9b7b38b1c943486bb1bf4b328fd48a6e`

The hands-on notes are `course-module-snellius-fs/README.md` at that commit. `episodes/files/ex1/print-n.c` and `episodes/files/ex1/run.sh` are copied from `course-module-snellius-fs/ex1/`. `episodes/files/PROVENANCE.md` records the same branch and commit.

The deck's table is the Snellius lifetime table: home 200 GiB, scratch-shared 14 days, scratch-local 6 days, scratch-node at job end, project and archive at project end. The worked `$TMPDIR` transcript (jobs `4401218` and `4401219` on `tcn386`) is from the README, not from a slide. The slide does not discuss metadata servers. That section is the reason the later file-count exercise is slow, taught here so the command is not the first time learners hear it.

## What to skip

Do not run the full `sbatch run.sh` (10^6 through 10^9 values, default directory home) on a small cluster. The tab has `iend=8 wdir=TMPDIR sbatch run.sh`.

Do not ask the course cluster for `--constraint=scratch-node`. The tab says the constraint is absent and `$TMPDIR` is already on the node disk.

The published job scripts name the `rome` partition. Leave those lines. The course cluster is a SURF Research Cloud workspace, and the course tab requests `--partition=rome`.

Do not generate 1000 files of 1 MB if `df -h` shows little free space. The optional challenge uses 100 files on the course cluster.

## Common mistakes

- Creating `/scratch-shared/$USER` on the course cluster. The path is not there. The tab names the scratch path.
- Treating `$TMPDIR` on the login node as the job's `$TMPDIR`. They are different directories. `wdir=TMPDIR` is a keyword the script expands inside the job.
- Leaving `ex1.dat` in home. The published script's default `wdir` is `$HOME`.
- `rmdir` on a non-empty directory, then reaching for `rm -r` on a path they have not printed.
- `chmod g-r` when the group read bit is already clear, and reading that as a broken `chmod`. Set `chmod 640` first so the change is visible.
- Reading the two `tcn386` paths as one directory. The job id in the name is `4401218` versus `4401219`.
- Assuming scratch-local and scratch-node expire the same way. The table gives scratch-local 6 days and scratch-node the end of the job.

## Prep checklist

- [ ] Confirm the machine. Put the scratch path from the tab on the board next to `/scratch-shared`.
- [ ] `myquota` works on Snellius, or `df -h` and `du -sh ~` work on the course cluster.
- [ ] Home has room for a few small text files. It does not need room for the full `print-n` run.
- [ ] From `episodes/files/ex1`, `module load 2025` and `module load GCC/14.2.0` succeed in a job shell. If `GCC/14.2.0` is absent, stop and check `module spider GCC`. Do not invent a version in the script during the room.
- [ ] On Snellius, only if you will run the scratch-node challenge: a node with the `scratch-node` feature is available. Otherwise teach the script and skip the submit.
- [ ] The optional file-set challenge is a choice you announce, not a default. Check free space first.

## What to collect

One `ls -l` mode string from `chmod g-r`, and one job output that prints both `$TMPDIR` and `realpath`. The job id will not be `4401218`. The shape of the two paths is the point.
