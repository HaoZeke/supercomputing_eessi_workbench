---
title: "Files and directories"
teaching: 10
exercises: 25
---

::: questions
- How do you see the directory you are in, and how do you make a directory on scratch?
- After `mv`, what does `ls` show?
- What does `rmdir` print when the directory is not empty?
:::

::: objectives
- Run `pwd`, `mkdir -p`, `cd`, and `ls` so an empty scratch directory prints nothing.
- Create a file, show it with `cat`, copy it, and rename it so `ls` shows only the new name.
- Remove an empty directory with `rmdir`, read the error on a non-empty directory, and remove it after emptying it.
:::

## The shell starts in home

Right after SSH, the current directory is your home directory. `pwd` prints that path. On Snellius it is `/home/$USER`. `cd` with no argument returns there from anywhere. `ls` prints the names in the current directory. An empty directory prints nothing. That empty print is success, not an error.

The scratch directory in the first task is not home. On Snellius it is `/scratch-shared/$USER`. `mkdir -p` creates it, and a second run does not fail if it is already there. The course cluster has no `/scratch-shared`. The tab names the scratch path you do have. Make your directory under that path. The `pwd` and `ls` checks are the same: `ls` of a new directory prints nothing.

::: sites scratch-places
:::

::: caution
## Login node

`pwd`, `mkdir`, and `cat` of one small file are what the login node is for. Do not generate a thousand files in this shell, and do not run the `print-n` program here. Those belong in the last episode, and they go through `sbatch`.
:::

::: callout
## Type along

Use the Snellius commands if your tab lists `/scratch-shared`. Otherwise use the scratch path in the tab, then the same `pwd` and `ls`.
:::

:::::::::::: challenge
## Task 1: make a scratch directory and show that it is empty

On Snellius:

``` bash
pwd
mkdir -p /scratch-shared/$USER
cd /scratch-shared/$USER
ls
pwd
cd
pwd
```

On the course cluster, `/scratch-shared` is not there. The tab names the scratch path. Create your directory under that path, `cd` into it, and run the same `ls` and `pwd`. Then `cd` with no argument.

::: solution
## Solution

`pwd` starts as `/home/<your-login>`.

`mkdir -p` creates the directory. On Snellius the path is `/scratch-shared/$USER`. On the course cluster it is a directory under the scratch path in the tab, not under `/scratch-shared`.

After `cd` into that directory, `pwd` prints it. `ls` prints nothing. No names, and no error, means the directory is empty.

`cd` with no argument returns to home. `pwd` prints `/home/<your-login>` again.
:::
::::::::::::

## A file you can show, copy, and rename

`touch` creates an empty file. An editor such as `nano` or `vim` puts text in it. `cat` prints the file. `printf` is a way to put one known line in the file without an interactive editor, so the later `cat` has an answer you can check.

`cp` copies. The original stays. `mv` changes the name. After `mv`, `ls` of that directory shows the new name and does not show the old name.

:::::::::::: challenge
## Task 2: copy, then rename

Start in home. On Snellius the scratch directory is `/scratch-shared/$USER`. On the course cluster, use the directory you created under the scratch path in the tab. The commands below say `SCRATCH`. Set it to that directory before you copy.

``` bash
cd
SCRATCH=/scratch-shared/$USER
printf 'one line\n' > notes.txt
cat notes.txt
mkdir -p "$SCRATCH"
cp notes.txt "$SCRATCH/notes.txt"
ls "$SCRATCH"
mv "$SCRATCH/notes.txt" "$SCRATCH/notes-kept.txt"
ls "$SCRATCH"
ls notes.txt
```

On the course cluster, set `SCRATCH` to the directory you created under the scratch path in the tab. Do not use `/scratch-shared/$USER` there.

::: solution
## Solution

`cat` prints:

``` text
one line
```

The first `ls` of the scratch directory prints `notes.txt`.

The `ls` after `mv` prints `notes-kept.txt` and does not print `notes.txt`. The new name is the only name in that directory.

The last `ls notes.txt` still finds the original in home. `cp` left it there. `mv` renamed only the copy.
:::
::::::::::::

## Directories, empty and not

`mkdir` creates a directory. `cd` enters it. `rmdir` removes a directory only when it is empty. That limit is useful. `rmdir` will not delete a tree of files because you pointed it at the wrong place.

If the directory still has a file, `rmdir` prints an error and leaves the directory in place. Remove the file, then run `rmdir` again.

:::: challenge
## Task 3: an empty directory

Run this in home.

``` bash
cd
mkdir demo-dir
cd demo-dir
pwd
ls
cd
rmdir demo-dir
ls
```

::: solution
## Solution

`pwd` inside `demo-dir` ends in `/demo-dir`. `ls` there prints nothing.

After `cd` back to home, `rmdir demo-dir` removes it because it is empty. The following `ls` does not list `demo-dir`.
:::
::::

:::: challenge
## Task 3 continued: rmdir refuses a file

``` bash
cd
mkdir demo-dir
cd demo-dir
touch keep.txt
cd ..
rmdir demo-dir
rm demo-dir/keep.txt
rmdir demo-dir
ls
```

What does the first `rmdir` print, and what is true after the second?

::: solution
## Solution

The first `rmdir` fails. The message is:

``` text
rmdir: failed to remove 'demo-dir': Directory not empty
```

`demo-dir` is still there, and `keep.txt` is still inside it. `rmdir` did not delete the file.

`rm demo-dir/keep.txt` empties the directory. The second `rmdir` then succeeds. `ls` in home does not list `demo-dir`.
:::
::::

::: keypoints
- `pwd` prints the current directory. A new shell starts in home.
- `mkdir -p /scratch-shared/$USER` is the Snellius scratch directory. The course cluster uses the path in the tab.
- `ls` of an empty directory prints nothing.
- After `mv`, `ls` shows the new name only. `cp` leaves the original.
- `rmdir` removes an empty directory. On a non-empty directory it errors, and it succeeds after you empty it.
:::
