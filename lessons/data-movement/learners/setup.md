---
title: Setup
---

You need a terminal with `bash`, `tar`, `rsync`, `sha256sum`, `split`, `dd`, `timeout`, and `cmp`.

Run the 20,000-file exercise from an empty directory on scratch. Home is the wrong place for that copy.

The stage exercise needs Slurm. The script in `episodes/files/stage.slurm` is the published ten-minute job. Submit it from scratch.

`mksquashfs` is the squashfs command in the pack episode. If it is missing, the `tar` exercise still stands.

`fpsync` comes from the fpart package. The `xargs` form in the several-streams episode does the same kind of copy.

mpiFileUtils is optional. EESSI 2023.06 and 2025.06 do not provide it. The episode tab is where that question stays for the machine in your welcome note.

The commands that leave the cluster use `snellius.surf.nl` as the SSH host and `archive.surf.nl` as the Data Archive login host.
