---
title: "Stage in, stage out"
teaching: 10
exercises: 20
---

::: questions

- Why does the copy back have to be inside the job script?
- Which seven checks does the deck list before you call a copy finished?

:::

::: objectives

- Stage inputs into `$TMPDIR` and copy results back to scratch before the job ends.
- Submit `stage.slurm`: partition `rome`, constraint `scratch-node`, ten minutes, one task.
- Apply the deck's seven-point checklist.

:::

## Around the job

Copy the inputs from scratch to `$TMPDIR`, which is the node disk. Write outputs there too. Copy the results back to scratch before the job ends: the node disk is removed for you. Then delete the scratch tree you no longer need.

```bash
rsync -a --partial \
  /scratch-shared/$USER/run/ $TMPDIR/run/
rsync -a --partial \
  $TMPDIR/out/ /scratch-shared/$USER/out/
```

After the results are back:

```bash
rm -rf /scratch-shared/$USER/run
srun drm --dryrun "$OLD"
srun drm "$OLD"
```

Use `srun drm` instead of `rm -rf` when the tree is large enough to stall one process. Run `drm --dryrun` first. `$OLD` is that tree.

::: callout

The copy back is inside the script. Once the job ends, the node disk is gone, and a second job has nothing to copy.

:::

The paths and the scratch constraint differ by machine. Read these before you edit a path into the script.

::: sites stage-paths
:::

::: sites scratch-node
:::

## A ten-minute job

Submit from scratch with `sbatch stage.slurm`. The file is `episodes/files/stage.slurm`. `--constraint=scratch-node` selects a node where `$TMPDIR` is the node disk. That disk is removed when the job ends, so the script copies the tree back to scratch before it exits.

```bash
#!/bin/bash
#SBATCH --job-name=stage
#SBATCH --partition=rome
#SBATCH --constraint=scratch-node
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --output=stage-%j.out
set -eu
rsync -a --partial \
  /scratch-shared/$USER/src/ "$TMPDIR/src/"
rsync -a --partial \
  "$TMPDIR/src/" /scratch-shared/$USER/out/
```

The published script requests partition `rome`, one node, and one task, for ten minutes. The second `rsync` is the copy back, and it is inside the script. It copies the staged `src` tree to `/scratch-shared/$USER/out/`.

The script already asks for one task. When a published script in the room asks for more cores than the node has, the override goes on the `sbatch` command line.

::: sites scale-two-core
:::

## Checklist

1. Pack small files with tar or mksquashfs before a wide copy.
2. Checksum the archive before the move and again after it.
3. Put the heavy copy on scratch, not in home.
4. Use `rsync -a --partial`, and run the same command again to resume.
5. Open several streams only for large files.
6. Stage into `$TMPDIR`, copy results out, then delete the scratch copy.
7. The Data Archive is not mounted on compute nodes. Run `daget` on a login or staging node first.

Point 6 is the one this script exists for. The copy out happens before the script exits.

:::::::::::: challenge

## Where the copy back goes

A job writes `result.txt` into `$TMPDIR` and exits. A second script, submitted afterwards, copies `$TMPDIR/result.txt` to scratch. What is missing, and which checklist point is it?

Then write the two `rsync` lines for the machine in your welcome note. The tab has the paths. Keep the copy back in the same script.

::: sites stage-paths
:::

::: sites scratch-node
:::

::: solution

## Solution

The node disk is removed when the job ends. The second script starts too late. Checklist point 6 says to stage into `$TMPDIR`, copy results out, then delete the scratch copy. Both `rsync` commands belong in the first script, in the order the tab shows: into `$TMPDIR`, then back to the shared path, before the script exits.

`stage.slurm` does that with the second `rsync` of `"$TMPDIR/src/"` onto `/scratch-shared/$USER/out/`. On a machine whose tab uses other paths, use those paths, and still keep the copy back inside the script. Add `--constraint=scratch-node` only when that tab says the node disk is selected that way.

:::

::::::::::::

:::: challenge

## Seven checks

A collaborator copies 20,000 small files with four `rsync` streams into home, skips the checksum, and reads `/archive/$USER` from a compute node. Which checklist points did they miss?

::: solution

## Solution

Point 1: pack the small files before a wide copy. Point 3: the heavy copy belongs on scratch. Point 2: checksum before the move and again after it. Point 5: several streams are for large files. Point 7: compute nodes do not mount the Data Archive, so `daget` on a login or staging node comes first.

:::

::::

::: keypoints

- `$TMPDIR` is the node disk. The job removes it on the way out.
- The copy back is a line in the same script, before the script exits.
- `stage.slurm` requests `rome`, `--constraint=scratch-node`, one task, and ten minutes.
- Pack, checksum, scratch, `rsync -a --partial`, large-file streams, stage out, and `daget` before a compute node. That is the checklist.

:::
