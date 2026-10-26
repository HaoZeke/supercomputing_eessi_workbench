---
title: "The EESSI client container"
teaching: 15
exercises: 15
---

::: questions
- How do you get the EESSI 2025.06 stack when you have no cluster login?
- What do `$EESSI_VERSION` and `$EESSI_CVMFS_REPO` print, and what does the CPU line mean?
- Which commands are missing inside the client?
:::

::: objectives
- Start the EESSI client with Apptainer and source the 2025.06 init script.
- Read `2025.06` from `$EESSI_VERSION` and `/cvmfs/software.eessi.io` from `$EESSI_CVMFS_REPO`.
- Treat `x86_64/intel/sapphirerapids` as one example CPU line, not as your required path.
- Show that `sbatch` is absent and that `python3 --version` still prints `Python 3.13.5`.
:::

## The same tree, no queue

The cluster episodes use a module command the site provides. When you have no login, the EESSI client container mounts the same CVMFS repository and gives you the same init script.

The client is an Apptainer container. Apptainer 1.0 or newer is required, with `--fusemount` support. The mount makes `/cvmfs/software.eessi.io` exist inside the container. That is why the init script path works. The image is `docker://ghcr.io/eessi/client:rocky8`.

There is no Slurm inside the container. `sbatch` and `squeue` are not installed. `hostname` prints the container's own name, not a cluster node. Use the container for `module` and `python3`. Use Snellius or the course cluster when the work must go through a queue.

The first launch downloads the image and can take a few minutes. Later launches are shorter.

::: instructor
## What to skip

If everyone is already on a cluster, do not spend the time downloading the image. The stack is already mounted. Read the two variable names, show one CPU line, and return to the modules.
:::

## Start the client

The directories under `$HOME/eessi-work` hold the CVMFS state and the home directory you see inside the container. The bind mounts give the container somewhere to write that state. You create them once.

::: callout
## Type along

Run the tab on a machine where Apptainer works. If you are already on Snellius or the course cluster, read the tab and do not start a second copy of the stack in this shell.
:::

::: sites client-container
:::

The Snellius and course-cluster tabs say you do not need the container there. The remaining tab is the launch. Inside the container, the next command is the init script:

``` bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
```

The script loads `EESSI/2025.06`. It prints that the module loaded, which CPU it selected, and whether it saw a GPU. One host printed:

``` text
Module for EESSI/2025.06 loaded successfully
EESSI has selected x86_64/intel/sapphirerapids as the compatible CPU target for EESSI/2025.06
EESSI did not identify an accelerator on the system
```

`x86_64/intel/sapphirerapids` is an example. A laptop, a different server, or another container host can print a different CPU. Read your line. Do not paste this example into `PATH`.

## Two variables that stay put

The CPU directory can change. Two variables do not:

``` bash
printf '%s\n' "$EESSI_VERSION"
printf '%s\n' "$EESSI_CVMFS_REPO"
```

`$EESSI_VERSION` prints `2025.06`. `$EESSI_CVMFS_REPO` prints `/cvmfs/software.eessi.io`.

If either line is empty, the init script did not run in this shell. Source it again. Do not also `module load 2025` here. The container has no module by that name, and stacking a second init on top of the first is the same mistake as loading two stacks.

Then load the default Python from the previous episode:

``` bash
module load Python/3.13.5-GCCcore-14.3.0
python3 --version
```

`python3 --version` prints `Python 3.13.5`. `which python3` starts with `/cvmfs/software.eessi.io/versions/2025.06/`.

::: caution
## Login node

This container is not a login node, and it is not a place to avoid the queue by running a long job. `python3 --version` is the check. A long script waits until you have `sbatch` on a cluster.
:::

:::: challenge
## Predict the two variables

Source the 2025.06 init script in the client. Before you print them, write down `$EESSI_VERSION` and `$EESSI_CVMFS_REPO`. Then run:

``` bash
printf '%s\n' "$EESSI_VERSION"
printf '%s\n' "$EESSI_CVMFS_REPO"
```

::: solution
## Solution

``` text
2025.06
/cvmfs/software.eessi.io
```

The first line is the stack the init script loaded. The second is the CVMFS repository, not a directory under your home. An empty line means the init script has not been sourced in this shell.
:::
::::

:::: challenge
## Your CPU line, not the example

Copy the CPU line the init script printed into your notes. Does it have to be `x86_64/intel/sapphirerapids`? What would go wrong if a job script hardcoded that directory?

::: solution
## Solution

It does not have to be `x86_64/intel/sapphirerapids`. That string is one host's example. Your line should contain a CPU target under `x86_64/` (or another architecture the script supports) and the words that name the compatible CPU.

A hardcoded `sapphirerapids` path fails on a machine whose init script selected a different CPU. The builds in that directory match the CPU that was detected, not the CPU written in someone else's notes. Let the init script select the directory.
:::
::::

:::: challenge
## No batch command, same Python

In the same container shell, after the init script:

``` bash
command -v sbatch || printf 'no-sbatch\n'
module load Python/3.13.5-GCCcore-14.3.0
python3 --version
```

What do the two output lines mean?

::: solution
## Solution

``` text
no-sbatch
Python 3.13.5
```

`command -v sbatch` prints nothing and returns a failure status, so the shell prints `no-sbatch`. The client has no Slurm. `squeue` is missing for the same reason.

`Python 3.13.5` is the EESSI 2025.06 default module, the same string as on a cluster that has `Python/3.13.5-GCCcore-14.3.0`. The stack matches. The queue does not. Submit jobs on Snellius or the course cluster, not in this shell.
:::
::::

::: keypoints
- The EESSI client is an Apptainer container that mounts `/cvmfs/software.eessi.io`.
- The init script is `source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash`.
- `$EESSI_VERSION` prints `2025.06`. `$EESSI_CVMFS_REPO` prints `/cvmfs/software.eessi.io`.
- The CPU line `x86_64/intel/sapphirerapids` is an example and may differ.
- The container has no `sbatch`. `python3 --version` still prints `Python 3.13.5`.
:::
