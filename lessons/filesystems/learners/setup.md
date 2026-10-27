---
title: "Setup"
---

You need a terminal and a login. The EESSI client container is the wrong place for this lesson. It has no `sbatch`, and the last episode submits a job.

## Snellius

Snellius is the Dutch national supercomputer. SURF sends the account mail. The public description is at <https://www.surf.nl/en/services/compute/snellius-the-national-supercomputer>.

``` bash
ssh YOUR_LOGIN@snellius.surf.nl
```

Sign in to the SURF user portal before the first SSH login. If the network you are on is not trusted, the welcome mail names a door node. Use that host.

Your prompt starts in home. `pwd` prints `/home/YOUR_LOGIN`.

## The course cluster

Your trainer sends a setup link and a welcome note. The note has the address and the login. There is one login node.

``` bash
ssh YOUR_LOGIN@MANAGER
```

`MANAGER` is the address in the welcome note. It is not `snellius.surf.nl`. Paths on this cluster are not the Snellius paths. Each episode's tab names the ones you have. Do not create `/scratch-shared` here. It is not on this machine.

## Files from this lesson

`episodes/files/ex1/print-n.c` and `episodes/files/ex1/run.sh` are the last episode's program. Submit from that directory, or copy both files into the directory you submit from. The script loads `module load 2025` and `GCC/14.2.0`.
