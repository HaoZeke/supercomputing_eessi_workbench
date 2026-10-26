---
title: "Reference"
---

## Commands

Start the 2025.06 stack where the repository is mounted:

``` bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
```

On the clusters, the first episode's tab gives the site command. It is `module load 2025` there. The container has no module named `2025`.

``` bash
module avail
module spider Python
module load Python/3.13.5-GCCcore-14.3.0
python3 --version
module list
module unload Python/3.13.5-GCCcore-14.3.0
module purge
```

`python3 --version` prints `Python 3.13.5` for `Python/3.13.5-GCCcore-14.3.0`.

After `module purge`, the 2023.06 stack is a different load. Do not load it on top of 2025.06.

``` bash
module load EESSI/2023.06
module load Python/3.11.5-GCCcore-13.2.0
python3 --version
```

That version line is `Python 3.11.5`.

Two variables set by the 2025.06 init script:

``` bash
printf '%s\n' "$EESSI_VERSION"
printf '%s\n' "$EESSI_CVMFS_REPO"
```

They print `2025.06` and `/cvmfs/software.eessi.io`.

## Glossary

EESSI
: European Environment for Scientific Software Installations. A shared stack of scientific builds, distributed with CVMFS.

CVMFS
: The file system that shows one directory tree on every machine that mounts it, and fetches a file the first time you use it. The tree in this lesson is `/cvmfs/software.eessi.io`.

shared stack
: One curated set of builds. You select a build by loading a module. The files stay on the shared tree.

module
: A name you load to put one build, and the libraries it needs, on your `PATH`.

Lmod
: The module command used by EESSI. `module` and, after the init script, `ml` both talk to it.

module avail
: Lists modules you can load right now. In a hierarchical stack that list is only the current level.

module spider
: Searches every module, including names that `module avail` hides until another module is loaded.

module load
: Puts one module into the current shell.

module unload
: Removes one module from the current shell.

module purge
: Removes all modules from the current shell. Run this before you switch stacks.

module list
: Prints the modules loaded in the current shell.

module whatis
: Prints the short description stored in a module file.

GCCcore
: The compiler build that a module was linked against. It is part of the module name, as in `Python/3.13.5-GCCcore-14.3.0`.

CPU target
: The processor family the init script selected, such as `x86_64/intel/sapphirerapids` on one host. Your line can name a different CPU.

Apptainer
: The container tool used to start the EESSI client. The client has modules and has no `sbatch`.

EasyBuild
: The tool that turns a recipe into a module file. Building modules is a different course.

QCG-PilotJob
: A site module on the clusters. It is not part of EESSI 2025.06. `module spider` inside the EESSI tree does not find it.
