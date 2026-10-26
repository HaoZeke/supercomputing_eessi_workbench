---
title: "Setup"
---

You need a terminal and one of the three machines below. You do not need all three.

## Snellius

Snellius is the Dutch national supercomputer. SURF sends the account mail after your project has a login. The public description of the machine is at <https://www.surf.nl/en/services/compute/snellius-the-national-supercomputer>.

``` {.bash org-language="sh"}
ssh YOUR_LOGIN@snellius.surf.nl
```

Sign in to the SURF user portal before the first SSH login. If the network you are on is not trusted, the welcome mail names a door node. Use that host instead of `snellius.surf.nl`.

A browser session through Open OnDemand is still a login node. Do not start the long run there.

## The course cluster

The course cluster is a Magic Castle workspace on SURF Research Cloud. The template is <https://github.com/ComputeCanada/magic_castle>. Your trainer sends a setup link. That link sets your password. The welcome note has the address, written here as `MANAGER`.

``` {.bash org-language="sh"}
ssh YOUR_LOGIN@MANAGER
```

There is one login node. `module load 2025` selects EESSI 2025.06. `module load 2024` selects that same stack and is the one you load before `QCG-PilotJob`. There is no CUA account and no project budget on this cluster.

## The EESSI client, when you have no cluster

The software episodes also run in the EESSI client container. Access is documented at <https://www.eessi.io/isc26-tutorial/getting-access/> and day-to-day use at <https://www.eessi.io/isc26-tutorial/usage/>.

You need Apptainer 1.0 or newer, with `--fusemount` support. This shell is the short form of the client script on that page. It mounts the same repository the cluster uses. It does not give you Slurm.

``` {.bash org-language="sh"}
mkdir -p "$HOME/eessi-work/var-lib-cvmfs" "$HOME/eessi-work/var-run-cvmfs" "$HOME/eessi-work/home"
export APPTAINER_BIND="$HOME/eessi-work/var-run-cvmfs:/var/run/cvmfs,$HOME/eessi-work/var-lib-cvmfs:/var/lib/cvmfs"
export APPTAINER_HOME="$HOME/eessi-work/home:/home/$USER"
apptainer shell --fusemount "container:cvmfs2 software.eessi.io /cvmfs/software.eessi.io" docker://ghcr.io/eessi/client:rocky8
```

Inside the container:

``` {.bash org-language="sh"}
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module load Python/3.13.5-GCCcore-14.3.0
python3 --version
```

`python3 --version` prints `Python 3.13.5`. The first launch downloads the image and can take a few minutes. Later launches are shorter.

::: callout
The container has no `sbatch` and no `squeue`. Use it for the software episode and for `pi_one.py`. Use Snellius or the course cluster for the queue.
:::

## Files from this lesson

The batch scripts and the pi program are in `episodes/files/`. Copy `pi_one.py` into the directory you submit from, or submit from `episodes/files` after you have cloned the lesson.
