---
title: "Reference"
---

## Snellius places

The course cluster does not have this list. Use the tab in the episode "The file systems".

| Place | Path | Backup | How long it lasts | Quota |
| --- | --- | --- | --- | --- |
| Home | `/home/$USER` | Yes, nightly | Project end, plus 15 weeks. Deleted files can be restored for three weeks | 200 GiB |
| Scratch-shared | `/scratch-shared/$USER` | No | 14 days | Counted in the 8 TiB scratch quota |
| Scratch-local | `$TMPDIR` | No | 6 days | Counted in the scratch quota |
| Scratch-node | `$TMPDIR` with `--constraint=scratch-node` | No | Removed when the job ends | No quota |
| Project | `/projects` | No | The life of the project | On demand |
| Archive | `/archive/$USER` | Yes | The life of the project | On demand, tape |

## Commands

``` bash
pwd
mkdir -p /scratch-shared/$USER
ls -l
chmod 640 mode-demo.txt
chmod g-r mode-demo.txt
myquota
df -h
du -sh ~
```

`chmod g-r` removes group read. A file that started as `-rw-r-----` becomes `-rw-------`.

A job directory:

``` bash
ls -l "$TMPDIR"
touch "$TMPDIR/testfile.foo"
echo "$TMPDIR"
realpath "$TMPDIR"
```

On Snellius, two jobs on node `tcn386` used `/scratch-local/scur1448.4401218` and `/scratch-local/scur1448.4401219`. `realpath` added `/gpfs/scratch1/nodespecific/tcn386/` in front of the same job directory.

From `episodes/files/ex1` on Snellius:

``` bash
sbatch run.sh
```

On a small cluster:

``` bash
iend=8 wdir=TMPDIR sbatch run.sh
```

`iend=8` writes 10^6 and 10^7 values. `wdir=TMPDIR` is a keyword the script expands inside the job. It is not the login node's `$TMPDIR`.

## Glossary

metadata server
: The part of a parallel file system that records names, owners, permissions, sizes, and where the bytes live. `ls` and creating a file talk to it.

data server
: The part that holds the bytes. Reading a large file talks to it after one metadata lookup.

inode
: One metadata record for one file. A quota can run out of inodes while bytes remain. Many small files spend inodes. One archive spends one.

home
: `/home/$USER`. Small, backed up, the right place for scripts and small inputs. On Snellius the quota is 200 GiB.

scratch-shared
: `/scratch-shared` on Snellius. Fast temporary space visible from the compute nodes. Unused data is removed after 14 days.

scratch-local
: Job space on the shared scratch file system, reached as `$TMPDIR`. On Snellius the path looks like `/scratch-local/$USER.$SLURM_JOB_ID`. The table gives it 6 days.

scratch-node
: NVMe on the node itself, on Snellius, requested with `--constraint=scratch-node`. Removed when the job ends. Not on every node. The course cluster does not have this constraint.

TMPDIR
: The environment variable that points at this job's scratch directory. It is a different directory on the login node and inside a job.

quota
: The cap on bytes, and often on inodes. On Snellius, `myquota` prints it. On the course cluster, `df -h` and `du -sh` are the tools.

mode string
: The ten characters `ls -l` prints for type and permissions. `chmod g-r` clears the group read bit.

project
: Shared space that lasts for the life of the project. `/projects` on Snellius. The course cluster tab names its own project path.

archive
: Slow, backed-up, long-term space on Snellius. The course cluster tab has no archive path.
