---
title: "Permissions and quota"
teaching: 10
exercises: 20
---

::: questions
- What does `chmod g-r` change in the mode string?
- How do you see whether home is close to full?
:::

::: objectives
- Read the ten-character mode string from `ls -l`.
- Remove group read with `chmod g-r` and read the new string.
- Run the quota command for your machine and name the home cap on Snellius.
:::

## The mode string

`ls -l` prints one line per file. The first field is the mode string. It has ten characters.

The first character is the type. `-` is a regular file. `d` is a directory.

The next nine characters are three groups of three: the owner, the group, and everyone else. Each group is `r`, `w`, `x`, or `-` when that permission is absent. `r` is read, `w` is write, `x` is execute.

``` text
- rw- r-- r--
```

with the spaces removed is `-rw-r--r--`. The owner can read and write. The group can read. Everyone else can read. Nobody can execute.

The numbers match the letters. Read is 4, write is 2, execute is 1. Add them inside one group. `rw-` is 6. `r--` is 4. `chmod 644` sets `-rw-r--r--`. `chmod 640` sets `-rw-r-----`: the owner can read and write, the group can read, and everyone else has nothing.

`chmod` can also change one letter. The form is who, then `+` or `-`, then the letter. `u` is the owner, `g` is the group, `o` is everyone else. `chmod g-r` means "group, remove, read". It does not change the owner, and it does not change everyone else.

A new file's starting string depends on the account. On Snellius the hands-on files in the source notes are `-rw-r-----`. Your file may already lack group read. Set a known mode first, then remove the bit, so the change is visible.

## Quota is a cap, not a suggestion

Home on Snellius is 200 GiB, with a limit a little above the quota, and a separate cap on inodes. Scratch is 8 TiB across scratch-local and scratch-shared. A full home stops the next copy. It also stops you writing the script that would move the data.

The command is in the tab. On Snellius it is `myquota`. On the course cluster, `myquota` identifies the home filesystem and reports shared BeeGFS capacity rather than a per-user quota. `df -h` prints size, used, and available for each mount you name. `du -sh ~` prints one total for home, not a line per file. `-s` is the summary. `-h` prints units you can read.

::: sites quota
:::

::: caution
## Do not fill home

A multi-gigabyte output does not belong in home. Home is 200 GiB on Snellius and it is backed up. A full quota stops the small edits too. Write large job output to scratch or to the project path, and remove a test file when the exercise is over.
:::

:::: challenge
## Task 4: chmod g-r

Run this in home.

``` bash
cd
printf 'one line\n' > mode-demo.txt
chmod 640 mode-demo.txt
ls -l mode-demo.txt
chmod g-r mode-demo.txt
ls -l mode-demo.txt
```

What is the mode string before `chmod g-r`, and what is it after?

::: solution
## Solution

After `chmod 640`, `ls -l` shows `-rw-r-----`. The type is `-`. The owner is `rw-`. The group is `r--`. Everyone else is `---`.

`chmod g-r` removes the group's `r`. The next `ls -l` shows `-rw-------`. The owner is unchanged. Everyone else is unchanged.

If your `ls -l` after `chmod 640` is not `-rw-r-----`, write down the string you do see. `chmod g-r` still only clears group read. The group column becomes `---` when it started as `r--`.
:::
::::

:::::::::::: challenge
## Task 5: read the quota

Run the command in the tab.

::: sites quota
:::

On Snellius, what is the home quota in GiB, and what else does the line count? On the course cluster, which commands replace `myquota`, and what does each print?

::: solution
## Solution

On Snellius, `myquota` prints a home line with `quota=200.00` in GiB. The limit in the documented example is `210.00`. `usage` is the fraction already used. The same line counts inodes: the documented quota is `1000000`. A scratch line is in TiB, with quota `8.00`, counted across scratch-local and scratch-shared.

On the course cluster, `myquota` reports the shared BeeGFS home capacity rather than a per-user quota. `df -h` prints one line per mount you named, with the size, the amount used, and the amount free. `du -sh ~` prints a single size for your home directory.

A home `usage` near the quota is the signal to move large files before the next job, not after the write has failed.
:::
::::::::::::

::: keypoints
- The mode string is type, then owner, group, and everyone else.
- `chmod 640` sets `-rw-r-----`. `chmod g-r` then sets `-rw-------`.
- Snellius home is 200 GiB. `myquota` prints the cap and the inode cap.
- Without `myquota`, `df -h` shows the mounts and `du -sh ~` shows home.
:::
