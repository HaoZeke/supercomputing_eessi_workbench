---
title: "A shared software stack"
teaching: 15
exercises: 10
---

::: questions
- Why do you load a module instead of installing a program into your home directory?
- What does the EESSI init script print, and which part of that printout can differ?
:::

::: objectives
- Describe a shared stack as one curated set of builds, selected with a module.
- Say what CVMFS fetches, and name the tree `/cvmfs/software.eessi.io`.
- Point to the EasyBuild book when the question is how a module was built, and stop there.
- Read the CPU line from the init script and leave a different CPU name alone.
:::

## One copy, many people

If every person compiles their own Python, the disk fills with almost the same files. Nobody can say which copy a paper used. A shared stack is one curated set of builds. You select a build by loading a module. The files stay on a shared file system. Your home directory stays for your own scripts and small inputs.

A cluster serves people from many fields. They need different programs, and often two versions of the same library. They also need builds tuned for the machine, not a binary that was packed for a laptop. Root access is restricted, so a private installer is the wrong tool even before the disk fills up.

Compiling from source, a Conda environment, and a container can each solve one person's problem. None of those is a way to support the whole machine. A local install is hard to patch for everyone, hard to tune once, and hard to name in a second paper. The module system is how the site hands out one supported copy.

## CVMFS fetches the file you use

EESSI is a shared stack of scientific builds, published by a group of European HPC sites so the same software can be loaded on more than one machine. It is distributed with CVMFS.

CVMFS shows a directory tree that is the same on every machine that mounts it. It fetches a file when you first use it. You do not copy the whole stack before you start. The tree for this lesson is `/cvmfs/software.eessi.io`.

![Where a program comes from. The nodes drawn are your script, CVMFS, EESSI, module, and the program.](fig/shared-stack.svg){alt='Where a program comes from. The nodes drawn are your script, CVMFS, EESSI, module, and the program.'}

Your script asks for a program. The module command points at a build in the EESSI tree. CVMFS supplies the file. You do not see a separate download step.

## EasyBuild is a different course

How those builds are produced is not this lesson. EasyBuild is the tool that turns a recipe into the module you load. Read that story in the book at <https://hpceb.rgoswami.me/> and in the sources at <https://github.com/HaoZeke/what-easybuild-is-doing>. This lesson only uses the result.

::: instructor
## What to skip

Do not open EasyBuild. Do not build a module from a recipe. Point at the book and move on.
:::

## Names for a stack

On Snellius the site stacks are named by year.

- `2025` is the production stack and is fully supported.
- `2024` is the previous production stack and has limited support.
- `2023` is deprecated and is provided as-is.
- `EESSI` is the common stack. It is a different row from the year names.

The command you type is not the same string on every machine. Read the tab for the machine in your welcome note before you assume a year name means one thing everywhere.

::: callout
## Type along

Follow the tab for the machine you are on. On a cluster the tab loads the stack with `module load`. In the client container the tab sources the init script, because that container has no module named `2025`.
:::

::: sites module-init
:::

Read the paragraph under the command in your tab.

On the course cluster, `module load 2025` loads EESSI 2025.06. The names `2024` and `foss/2023a` load that same stack, so an older script still starts. On Snellius, `module load 2025` selects the 2025 site stack. In the container there is no module named `2025`. The init script is the command there:

``` bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
```

That script loads `EESSI/2025.06` and prints three kinds of lines: that the module loaded, which CPU target it selected, and whether it saw a GPU. On one Intel host the lines were:

``` text
Module for EESSI/2025.06 loaded successfully
EESSI has selected x86_64/intel/sapphirerapids as the compatible CPU target for EESSI/2025.06
EESSI did not identify an accelerator on the system
```

The CPU line is an example. Your line may name a different CPU. Read the line. The init script picks the directory. Do not copy a path from someone else's CPU into your script.

The client is the same repository, with no queue. Use it when you have no cluster login. Skip the download when you are already on a cluster.

::: sites client-container
:::

The previous EESSI stack is still published. After `module purge`, `module load EESSI/2023.06` switches to it. You can also source `/cvmfs/software.eessi.io/versions/2023.06/init/lmod/bash` in a new shell. Do not load both stacks in one shell. Purge first. The next episode loads Python from one stack at a time.

:::: challenge
## Where a private copy fails

A lab mate wants to `pip install` a scientific package into their home directory so the paper has a private copy. Name one problem that causes on a shared machine. Where do you send the question "how was this module built?"

::: solution
## Solution

A private copy fills home, drifts away from the copy the next person loads, and cannot be named as one module in two papers. Support cannot patch every home directory. The question about how the module was built goes to the EasyBuild book at <https://hpceb.rgoswami.me/>, not to a second install in this lesson.
:::
::::

:::: challenge
## Read the CPU line

You sourced the 2025.06 init script. It printed a CPU target. A neighbour's notes say `x86_64/intel/sapphirerapids`. Yours names a different CPU. Which line do you keep, and what do you not paste into a job script?

::: solution
## Solution

Keep the line your own init script printed. `x86_64/intel/sapphirerapids` is one host's example, not a required value. The path under `/cvmfs/software.eessi.io/versions/2025.06/` contains that CPU directory. The init script chooses it. Pasting a neighbour's CPU directory into `PATH` or into a script points at builds that may not match your machine.
:::
::::

::: keypoints
- A shared stack is one supported copy of a program, selected with a module.
- CVMFS shows `/cvmfs/software.eessi.io` and fetches a file when you first use it.
- EasyBuild, and how a module file is produced, is the book at <https://hpceb.rgoswami.me/>.
- The init script prints a CPU target. The example `x86_64/intel/sapphirerapids` can differ.
- `module purge` before you switch stacks. Do not load two stacks in one shell.
:::
