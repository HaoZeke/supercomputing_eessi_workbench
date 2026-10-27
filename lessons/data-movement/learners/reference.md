---
title: Glossary
---

Manual pages named by the deck: `man rsync`, `man tar`, `man sha256sum`, and `man mksquashfs`.

mpiFileUtils manual: <https://mpifileutils.readthedocs.io/> (`dwalk`, `dcp`, `dsync`, `drm`, `dtar`).

SURF pages, by the topic the deck names:

- Connecting to the system. The SSH host is `snellius.surf.nl`.
- Data Archive from Snellius. Tools and paths: `daget`, `/archive`, partition `staging`. Login host: `archive.surf.nl`.
- How to use Rclone with Research Drive. The remote in the example is `RD`.
- Snellius filesystems. Names from the deck: `$TMPDIR`, `scratch-node`.
- An mpiFileUtils easyconfig, for a site that provides no module. The course cluster already has mpiFileUtils installed.

## Glossary

metadata server
: Records each create, open, and close. A million small files queue here while the data servers wait.

data server
: Moves the bytes of a file.

home
: Directory for code and notes.

scratch
: Place for the heavy copy.

project
: File system for a group's long-lived data.

node disk
: Disk on the compute node. Inside a job it is `$TMPDIR`. It is removed when the job ends.

partial file
: The incomplete file `--partial` leaves behind so the next `rsync` continues.

checksum
: The `sha256sum` record of an archive. `sha256sum -c` prints `src.tar: OK` when the bytes match.

squashfs
: One file, built with `mksquashfs -comp zstd`, that you can mount read-only.

mpiFileUtils
: MPI programs for a large tree: `dwalk`, `dcp`, `dsync`, `drm`, `dtar`. EESSI 2023.06 and 2025.06 do not provide them. The course cluster has them installed.

Data Archive
: Tape at `/archive/$USER` on Snellius login and staging nodes. Compute nodes do not mount `/archive`. The login host is `archive.surf.nl`.
