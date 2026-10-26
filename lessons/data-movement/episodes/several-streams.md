---
title: "Several streams"
teaching: 15
exercises: 10
---

::: instructor

This episode is optional.

:::

::: questions

- When do four copy streams help?
- What does each mpiFileUtils program do, and where does the deck's job script run it?

:::

::: objectives

- Run four `rsync` processes with `xargs -P 4` or `fpsync -n 4` on large shards.
- Name `dwalk`, `dcp`, `dsync`, `drm`, and `dtar`, and match each one to the job it does.
- Read `dcp.slurm`: partition `rome`, 2 nodes, 8 tasks per node.

:::

## Four streams, for large files

Four streams help when each shard is a large file. A million tiny files still need a pack first. `xargs -P` and `fpsync` (from the fpart package) both run several `rsync` processes.

`--exclude` skips build products. The destination tree must already exist for the `xargs` form, because each call writes one shard.

```bash
printf '%s\0' shard-*/ |
  xargs -0 -P 4 -I{} \
  rsync -a --partial {}/ \
  /scratch-shared/$USER/copy/{}/
```

`fpsync` is a separate command from the exclude example. The exclude line is an ordinary `rsync`.

```bash
fpsync -n 4 -o '-a --partial' \
  /scratch-shared/$USER/run/ \
  /scratch-shared/$USER/copy/
rsync -a --partial --exclude '*.o' \
  --exclude '.git/' run/ dest/
```

## mpiFileUtils inside a Slurm job

These are MPI programs from the mpiFileUtils suite. `srun` starts one of them across the tasks in the job. The options below are from the project manual.

- `dwalk -v` counts files and bytes.
- `dcp -p` copies and keeps permissions, group, and timestamps.
- `dsync` makes the destination match the source.
- `drm --dryrun` lists what a recursive delete would remove.
- `dtar -c` writes a pax archive.

```bash
srun dwalk -v "$SRC"
srun dcp -p "$SRC" "$DST"
srun dsync -v "$SRC" "$DST"
srun drm --dryrun "$OLD"
srun dtar -c -f run.tar run/
```

The manual is <https://mpifileutils.readthedocs.io/>.

EESSI 2023.06 and 2025.06 do not provide mpiFileUtils. Snellius loads a site module or builds it with EasyBuild. The course cluster has mpiFileUtils installed, and that install is not an EESSI module. The tab has the commands for the machine in your welcome note.

::: sites mpifileutils
:::

## Two Rome nodes

The published script walks the source and copies it. The slide text also says the job walks the copy. The script block on the slide, which is `episodes/files/dcp.slurm`, ends at `dcp`.

Snellius uses the `rome` partition for these CPU nodes. Submit with `sbatch dcp.slurm` from a directory on scratch, so the heavy tree stays off home.

```bash
#!/bin/bash
#SBATCH --job-name=dcp
#SBATCH --partition=rome
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --time=01:00:00
#SBATCH --output=dcp-%j.out
set -eu
SRC=/scratch-shared/$USER/run
DST=/scratch-shared/$USER/run-copy
srun dwalk -v "$SRC"
srun dcp -p "$SRC" "$DST"
```

That is 2 nodes and 8 tasks per node, and a one-hour limit. The partition line in the file is the published Snellius line. The tab is the request for the machine in your welcome note. The scripts stay as published.

::: sites partition-request
:::

:::: challenge

## Large files, or a million small ones

You have four disks' worth of bandwidth and a directory of a million tiny files. What do you do before you open four `rsync` streams?

::: solution

## Solution

Pack the tiny files first. Four streams help when each shard is a large file. They leave the metadata server with a million creates if you point them at a million tiny files.

:::

::::

:::::::::::: challenge

## Submit the published copy

`episodes/files/dcp.slurm` is the job. Which partition, node count, and tasks per node does the file request? Then read the tabs before you change a line for the machine in your welcome note.

::: sites partition-request
:::

::: sites mpifileutils
:::

::: solution

## Solution

The file requests partition `rome`, `--nodes=2`, and `--ntasks-per-node=8`. Submit it from scratch with `sbatch dcp.slurm`.

EESSI 2023.06 and 2025.06 do not provide mpiFileUtils. On the course cluster it is installed, and it is not an EESSI module. The partition tab is the request for this machine. Leave the script's partition line as published.

:::

::::::::::::

::: keypoints

- `xargs -P 4` and `fpsync -n 4` run several `rsync` processes.
- Several streams help large files. Pack a million tiny files first.
- `dwalk` counts, `dcp -p` copies, `dsync` matches the destination to the source, `drm --dryrun` lists a delete, and `dtar -c` writes a pax archive.
- `dcp.slurm` asks for the `rome` partition, 2 nodes, and 8 tasks per node.
- EESSI 2023.06 and 2025.06 do not provide mpiFileUtils. The course cluster has it installed, and that install is not an EESSI module.

:::
