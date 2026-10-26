---
title: Instructor notes
---

## Timing

| Episode | Teaching | Exercises |
| --- | --- | --- |
| Why copying hurts | 10 | 0 |
| Pack, then checksum | 10 | 15 |
| rsync | 10 | 15 |
| Several streams (optional) | 15 | 10 |
| From outside the cluster | 10 | 5 |
| Stage in, stage out | 10 | 20 |

Several streams is optional. Skip it when the room is tight, and keep the pack, rsync, and stage exercises.

## Deck

Branch `feat/data-movement-deck`, commit `f7ed5319a86448ac8dda3cb60fe4f58f64b5ca09`.

The file is `slides-data-movement/data-movement.org`, Rohit Goswami, 26 October 2026. `PROVENANCE.md` records the same pair. The three scripts under `episodes/files/` are the sequences on the slides.

## Prep

Give the room an empty directory on scratch before `predict.sh`. The script creates 20,000 one-line files plus a tar archive. Home is the wrong disk for that.

The ext4 note on the deck (26 October 2026) says the order matches the prediction, the partial file was 4128768 bytes of 50331648, and `sha256sum -c` printed `src.tar: OK`. It does not record the three `real` times. Ask the room to write down their own `real` line. Do not fill in seconds.

`stage.slurm` is a ten-minute job. Submit it from scratch. The copy back is the second `rsync`, and it has to run inside that script.

The published scripts name the `rome` partition, and `stage.slurm` also sets `--constraint=scratch-node`. Leave those lines as published. The site tabs are what you show for the machine in the welcome note. The course cluster is a SURF Research Cloud workspace, and the course tab requests `--partition=rome`.

EESSI 2023.06 and 2025.06 do not provide mpiFileUtils. The course cluster has it installed. That install is not an EESSI module. The course tab shows the commands.

`fpsync` needs fpart. If it is absent, teach the `xargs -P 4` form and move on.

`mksquashfs` may be absent. The timed exercise uses `tar`.

## Common mistakes

- Treating a slow `cp -r` of the 20,000 files as a network problem. The metadata server is doing a create for every file.
- Running `predict.sh` in the lesson directory or in home.
- Dropping the trailing slash on the `rsync` source and then looking for files one directory too deep.
- Reading `part/big.bin` after `timeout` as a finished copy. `cmp` is the check, and it prints nothing when the bytes match.
- Putting the copy back in a second job. The node disk is already gone.
- Opening four streams on the tiny files. Pack those first. Four streams are for large shards.
- Expecting `scp` to continue a partial file. It starts again from the first file.
- Assuming `/archive` is visible on a compute node. `daget` runs on a login or staging node. The deck's copy onto scratch uses the `staging` partition.
