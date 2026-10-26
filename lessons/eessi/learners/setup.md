---
title: "Setup"
---

You need a terminal. You need one of the three places below. You do not need all three.

## Snellius

Snellius is the Dutch national supercomputer. SURF sends the account mail. The public description is at <https://www.surf.nl/en/services/compute/snellius-the-national-supercomputer>.

``` bash
ssh YOUR_LOGIN@snellius.surf.nl
```

Sign in to the SURF user portal before the first SSH login. If the network you are on is not trusted, the welcome mail names a door node. Use that host.

`module load 2025` selects the 2025 stack. The first episode has the load lines for each machine.

## The course cluster

Your trainer sends a setup link and a welcome note. The note has the address and the login. There is one login node.

``` bash
ssh YOUR_LOGIN@MANAGER
```

`MANAGER` is the address in the welcome note. It is not `snellius.surf.nl`. `module load 2025` loads EESSI 2025.06 on this cluster. The first episode's tab has the exact lines.

## The EESSI client, when you have no cluster

You need Apptainer 1.0 or newer, with `--fusemount` support. Access is documented at <https://www.eessi.io/isc26-tutorial/getting-access/> and day-to-day use at <https://www.eessi.io/isc26-tutorial/usage/>.

The client mounts the same CVMFS repository the stack is published on. It does not start a queue.

::: sites client-container
:::

After the init script from that tab:

``` bash
module load Python/3.13.5-GCCcore-14.3.0
python3 --version
```

`python3 --version` prints `Python 3.13.5`. The first launch downloads the image and can take a few minutes. Later launches are shorter.

::: caution
## No queue in the container

The container has no `sbatch` and no `squeue`. Use it for these software episodes. Use Snellius or the course cluster when the work has to wait in a queue.
:::
