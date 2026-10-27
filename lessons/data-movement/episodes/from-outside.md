---
title: "From outside the cluster"
teaching: 10
exercises: 5
---

::: questions

- What does `scp` do when the transfer stops, and what does `rsync` do?
- Where is `/archive/$USER` mounted, and what has to happen before a compute node can read that tree?

:::

::: objectives

- Continue a partial copy with `rsync`, and recognise that `scp` starts over.
- Name Globus, iRODS iCommands, `daget`, and an rclone WebDAV remote for Research Drive.
- Keep the Data Archive on login and staging nodes, which are the nodes that mount `/archive`.

:::

## From your own computer

`scp` starts again from the first file if the transfer stops. `rsync` continues a partial file. Globus moves between endpoints you registered. On Snellius, the iRODS iCommands below are the documented 2023 modules. The Data Archive is `/archive/$USER` on login and staging nodes only. `daget` stages tape, and compute nodes do not mount `/archive`. Research Drive works as an rclone WebDAV remote. SURF documents the setup.

`SRC` and `DEST` are Globus endpoints you registered. `RD` is the rclone remote in the SURF Research Drive example.

```bash
scp -r run/ USER@snellius.surf.nl:/scratch-shared/$USER/run
rsync -a --partial --info=progress2 run/ \
  USER@snellius.surf.nl:/scratch-shared/$USER/run/
globus transfer SRC:run/ DEST:run/
module load 2023
module load iRODS-iCommands/4.3.0
iput -r run
daget /archive/$USER/run
srun -t 1:00:00 -p staging cp -r /archive/$USER/run /scratch-shared/$USER/
rclone copy run/ RD:run/
```

`snellius.surf.nl` is the SSH host. `archive.surf.nl` is the Data Archive login host.

The `srun` line is one hour on the `staging` partition. It copies from `/archive/$USER/run` onto `/scratch-shared/$USER/`. Run `daget` on a login or staging node first. A compute node has no `/archive` mount, so a job there cannot open that path.

The SURF pages, by topic:

- Connecting to the system, host `snellius.surf.nl`.
- Data Archive from Snellius: `daget`, `/archive`, partition `staging`, login host `archive.surf.nl`.
- How to use Rclone with Research Drive, remote `RD`.
- Snellius filesystems: `$TMPDIR` and `scratch-node`, used in the next episode.

:::: challenge

## The transfer stops halfway

You started `scp -r run/ USER@snellius.surf.nl:/scratch-shared/$USER/run` and the connection dropped. You still have a partial tree on scratch. Which command continues that partial copy, and which command starts again from the first file?

::: solution

## Solution

`rsync -a --partial --info=progress2` continues a partial file. Run the same command again. `scp` starts again from the first file if the transfer stops.

:::

::::

::: keypoints

- `scp` starts again from the first file. `rsync -a --partial` continues.
- Globus uses endpoints you registered (`SRC`, `DEST`). iRODS iCommands on Snellius are the 2023 modules `iRODS-iCommands/4.3.0`.
- `/archive/$USER` is on login and staging nodes. `daget` stages tape. Compute nodes do not mount `/archive`.
- `archive.surf.nl` is the Data Archive login host. `snellius.surf.nl` is the SSH host.
- Research Drive is an rclone WebDAV remote named `RD` in the SURF example.

:::
