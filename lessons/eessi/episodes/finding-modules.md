---
title: "Finding and loading a module"
teaching: 20
exercises: 20
---

::: questions
- Which command lists only the modules you can load right now, and which command searches the rest?
- Which Python module is the EESSI 2025.06 default, and what does `python3 --version` print?
- Where do you load `QCG-PilotJob` if `module spider` cannot find it in EESSI?
:::

::: objectives
- Use `module avail`, `module spider`, `module load`, `module list`, `module unload`, and `module purge`.
- Load `Python/3.13.5-GCCcore-14.3.0` and read `Python 3.13.5`.
- Switch to EESSI 2023.06 only after a purge, and read `Python 3.11.5`.
- State that `QCG-PilotJob` is a site module and is not in the EESSI tree.
:::

## Two lists

`module avail` prints modules you can load in this shell, right now. EESSI is hierarchical. A Python build sits behind the stack module, and often behind a compiler module. Until those are loaded, `module avail Python` can be empty or short. That does not mean Python is missing.

`module spider` searches the whole tree. It finds names that `module avail` hides. `module spider Python` is the search you want when you know the program and not the compiler.

`module help` prints the command options. `module whatis Python/3.13.5-GCCcore-14.3.0` prints the short description stored in that module file. `module list` prints what this shell has loaded. `ml` is the short form of `module` once the init script has run. `ml Python` is the same action as `module load Python`.

| Command | What it does |
| --- | --- |
| `module avail` | Modules you can load right now |
| `module spider` | Every matching module, including hidden ones |
| `module load` | Puts a module in this shell |
| `module unload` | Removes one module |
| `module list` | Shows what is loaded |
| `module purge` | Removes all modules |
| `module whatis` | Prints the module's short description |

## One Python from the 2025.06 stack

Load the stack the way your tab shows, then search.

::: sites module-python
:::

In EESSI 2025.06 the Python modules include:

- `Python/3.12.3-GCCcore-13.3.0`
- `Python/3.13.1-GCCcore-14.2.0`
- `Python/3.13.5-GCCcore-14.3.0` (the default)

The name has the version and the `GCCcore` it was built with. Load the default:

``` bash
module load Python/3.13.5-GCCcore-14.3.0
python3 --version
```

`python3 --version` prints `Python 3.13.5`. `which python3` prints a path under `/cvmfs/software.eessi.io/versions/2025.06/`. The CPU directory in the middle of that path is the one the init script chose. It is not `/usr/bin/python3`.

On Snellius, `module load 2025` selects the site 2025 stack. If `module spider Python` does not list `Python/3.13.5-GCCcore-14.3.0`, load the newest 3.13 it does list and write that full name in your notes. Do not invent a version.

A faded load, for the stack this course uses:

``` bash
module load Python/________
python3 --version
```

The module is `Python/3.13.5-GCCcore-14.3.0`. The version line is `Python 3.13.5`.

## Unload one, or clear the shell

`module unload Python/3.13.5-GCCcore-14.3.0` removes that Python. The stack module can stay loaded. `module list` no longer includes the Python name.

`module purge` removes every module. `module list` then reports that no modules are loaded. Purge is the step between stacks.

EESSI 2023.06 has `Python/3.11.5-GCCcore-13.2.0`. After a purge:

``` bash
module load EESSI/2023.06
module load Python/3.11.5-GCCcore-13.2.0
python3 --version
```

`python3 --version` prints `Python 3.11.5`. Do not load `EESSI/2025.06` and `EESSI/2023.06` in one shell. Do not source the 2025.06 init script and then `module load 2025` on top of it. Two stacks in one shell is how two Pythons end up on `PATH`.

::: callout
## Conda stays separate

A Conda environment and a loaded module often conflict. The site stack is the supported copy. Do not mix a Conda `activate` with these modules in the same shell.
:::

## QCG-PilotJob is not in EESSI

`module spider QCG-PilotJob` in an EESSI-only shell does not find it. The tool is not part of the 2025.06 release. Do not spend the episode walking the CVMFS tree looking for it.

On the clusters it is a site module. The load line is the tab, not a path you guess.

::: sites qcg-modules
:::

Course scripts name `QCG-PilotJob/0.14.1-gfbf-2024a` after the stack load. If spider prints that name, load it. If spider prints a different full name, load the name it prints. The container will still not have it. Later episodes that need the pilot use the cluster.

::: caution
## Login node

`python3 --version` and `module list` are fine on the login node. A long Python script is not. The login node is shared. Send the long run to the queue.
:::

:::: challenge
## Predict the version lines

Write down the two version lines before you run the block. Use a shell you are allowed to purge.

In the container, or on any machine where `/cvmfs/software.eessi.io` is mounted:

``` bash
module purge
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module load Python/3.13.5-GCCcore-14.3.0
python3 --version
module purge
module load EESSI/2023.06
module load Python/3.11.5-GCCcore-13.2.0
python3 --version
```

On a cluster, do not source the init script in a shell where you also ran `module load 2025`. Use the tab's load command for the 2025 stack, check `python3 --version`, purge, and only then try `EESSI/2023.06`. If that module name does not exist on Snellius, stop. Do not load a second stack on top of the first.

::: solution
## Solution

In the EESSI client the two `python3 --version` lines are:

``` text
Python 3.13.5
Python 3.11.5
```

The first comes from `Python/3.13.5-GCCcore-14.3.0` on EESSI 2025.06. The second comes from `Python/3.11.5-GCCcore-13.2.0` on EESSI 2023.06. `module purge` between them is required. `which python3` for the first load starts with `/cvmfs/software.eessi.io/versions/2025.06/`.

On Snellius, if the 3.13.5 module name is absent, the version line is the one for the module you actually loaded. Record that name. A missing `EESSI/2023.06` is a stop, not a reason to skip the purge.

If the init script stops because a variable is unset, run `set +u` before `source` and `set -u` afterwards. The two version lines do not change.
:::
::::

:::: challenge
## List, unload, purge

Load the 2025.06 default Python. Run `module list`. Unload that Python module and run `module list` again. Purge and run `module list` a third time. What happens to the Python name?

::: solution
## Solution

After the load, `module list` includes `Python/3.13.5-GCCcore-14.3.0`. Other modules may be there too, because loading Python also loads the libraries it needs. That is expected.

After `module unload Python/3.13.5-GCCcore-14.3.0`, that name is gone. The stack module can still be listed.

After `module purge`, `module list` reports that no modules are loaded. The next `python3` is no longer the stack copy unless something else on `PATH` provides one.
:::
::::

:::: challenge
## Search for a module that is not in the stack

Run `module spider QCG-PilotJob` in a shell that has only EESSI loaded. Then look at the tab above and say where the tool actually comes from.

::: solution
## Solution

Spider reports that it cannot find `QCG-PilotJob` in the EESSI tree. That result is correct. The tool is not in the 2025.06 release.

On a cluster, load it the way the tab shows: the stack name first (`module load 2025` on Snellius, `module load 2024` on the course cluster), then `module load QCG-PilotJob`. `module list` then includes `QCG-PilotJob`. The full name in the course scripts is `QCG-PilotJob/0.14.1-gfbf-2024a` when spider lists that name.

The container has no site module to add. A failed spider search there does not mean you should install a private copy during this lesson.
:::
::::

::: keypoints
- `module avail` is the current level. `module spider` searches the rest.
- `module load` selects. `module unload` removes one. `module purge` clears the shell.
- EESSI 2025.06 default Python is `Python/3.13.5-GCCcore-14.3.0`, and `python3 --version` prints `Python 3.13.5`.
- EESSI 2023.06 has `Python/3.11.5-GCCcore-13.2.0`. Purge before you load it.
- `QCG-PilotJob` is a site module. Spider does not find it in EESSI.
:::
