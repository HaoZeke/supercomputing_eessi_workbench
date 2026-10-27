---
title: "Space for a job"
teaching: 15
exercises: 25
---

::: questions
- What does a job's `$TMPDIR` look like, and why do two jobs on one node get two directories?
- How do you ask Snellius for scratch-node, and what do you do on a cluster that has no such disk?
- How do you shrink `ex1/run.sh` without editing it?
:::

::: objectives
- Submit a job that lists `$TMPDIR`, creates a file there, and prints `realpath`.
- Read the `tcn386` transcript: job `4401218` and job `4401219` are two directories on one node.
- Request scratch-node on Snellius, and follow the tab where that constraint does not exist.
- Run `print-n` for 10^6 to 10^9 values on Snellius, or `iend=8 wdir=TMPDIR sbatch run.sh` on a small cluster.
:::

## The directory belongs to the job

`$TMPDIR` inside a job is a directory the scheduler created for that job. It is not the login node's `/tmp`, and it is not the login node's `$TMPDIR`. Write scratch files there. Copy anything you must keep to a path that lasts, before the script exits.

The tab says what the variable points at on your machine.

::: sites tmpdir
:::

On Snellius, a compute-node `$TMPDIR` is `/scratch-local/$USER.$SLURM_JOB_ID`. `realpath` prints the GPFS path under `/gpfs/scratch1/nodespecific/<node>/`. Two jobs on the same node get two directories. The job id is in the name. On the course cluster, `$TMPDIR` is on the node's own disk and is deleted when the job ends. There is one login node, so the comparison is the login node's `/tmp` against a job's `$TMPDIR`, not two login nodes.

This script is the check. It prints the node, lists the directory, creates one empty file, lists again, and prints both the variable and `realpath`.

``` bash
#!/bin/bash
#SBATCH -J files
#SBATCH -t 5
#SBATCH -p rome

hostname
ls -l $TMPDIR
touch "$TMPDIR/testfile.foo"
ls -l $TMPDIR
echo $TMPDIR
realpath $TMPDIR
```

`-t 5` asks for five minutes. `-J files` is the job name. The script's partition line is `-p rome`, as published. Leave that line as it is in the file. Submit the file with `sbatch`. Do not run it with `bash` on the login node.

The source notes recorded two submits that both ran on `tcn386`. The output files were `slurm-4401218.out` and `slurm-4401219.out`.

``` text
tcn386.local.snellius.surf.nl
total 0
total 0
-rw-r----- 1 scur1448 scur1448 0 Nov  9 00:25 testfile.foo
/scratch-local/scur1448.4401218
/gpfs/scratch1/nodespecific/tcn386/scur1448.4401218
```

``` text
tcn386.local.snellius.surf.nl
total 0
total 0
-rw-r----- 1 scur1448 scur1448 0 Nov  9 00:25 testfile.foo
/scratch-local/scur1448.4401219
/gpfs/scratch1/nodespecific/tcn386/scur1448.4401219
```

Read it from the top. `hostname` is the compute node, `tcn386`, not a login node. The first `ls -l` prints `total 0` and no file. The directory was empty. The second `ls -l` prints `total 0` and then `testfile.foo`. `touch` created an empty file, so the size is 0. The mode `-rw-r-----` is the mode from the previous episode.

`echo $TMPDIR` prints `/scratch-local/scur1448.<jobid>`. `realpath` prints `/gpfs/scratch1/nodespecific/tcn386/scur1448.<jobid>`. Those are two names for one directory. The job id changes. The node in this pair does not: both jobs ran on `tcn386`.

Scratch-local can still be listed after the job has written the file. It counts against the scratch quota until it expires. The table in the previous episode gives it 6 days. From a Snellius login node the source notes listed leftover directories with:

``` bash
ls -ld /gpfs/scratch1/nodespecific/*/scur1448.*
```

That printed three directories on `tcn386`, for jobs `4401213`, `4401218`, and `4401219`. Your login replaces `scur1448`. Do not run that `ls` on the course cluster. There is no `/gpfs/scratch1/nodespecific` there.

::: caution
## Login node

Submit the script. Do not execute it on the login node. A write there uses the shared login node, and the temporary directory you see is not the job's `$TMPDIR`.
:::

:::: challenge
## Read the two job outputs

Using only the transcript above: did the two jobs share a node? Did they share a directory? Which printed path is the GPFS path?

::: solution
## Solution

They shared a node. Both hostnames are `tcn386.local.snellius.surf.nl`.

They did not share a directory. The ids are `4401218` and `4401219`. Same node, two job directories.

The GPFS path is the `realpath` line, `/gpfs/scratch1/nodespecific/tcn386/scur1448.<jobid>`. The `/scratch-local/...` line is the other name for that same directory.
:::
::::

:::: challenge
## Submit the TMPDIR job

Put the script in a file, `files-tmpdir.sh`, and submit it:

``` bash
sbatch files-tmpdir.sh
```

When the output file appears, compare it with the `tcn386` transcript. Your job id and your node name will differ.

::: solution
## Solution

The output has six parts:

1. A compute-node hostname, not your login node.
2. `total 0` from the first `ls -l`, with no filename.
3. `total 0` and `testfile.foo` from the second `ls -l`. The size is 0 because `touch` creates an empty file.
4. `echo` printing `$TMPDIR`.
5. `realpath` printing another absolute path for that same directory.

On Snellius the two paths look like `/scratch-local/$USER.<jobid>` and `/gpfs/scratch1/nodespecific/<node>/$USER.<jobid>`. A second submit gets a new job id in the name, even on the same node.

On the course cluster the path is the one in the `$TMPDIR` tab, on the node's disk, and the directory is removed when the job ends. The output file from `sbatch` remains in the directory where you submitted. That file is how you read the path after the job.
:::
::::

## Scratch-node ends with the job

Scratch-node is the same idea on a faster disk, and only on Snellius. The disk is NVMe on the node. `$TMPDIR` points at your directory on it. The directory is removed when the job ends. There is no quota. Copy results off before the script exits. The node feature is not universal, so the script asks for it.

::: sites scratch-node
:::

The course cluster has no `--constraint=scratch-node`. `$TMPDIR` is already on the node's disk. Drop the constraint and still write to `$TMPDIR`.

:::::::::::: challenge
## Write one file on the fast disk

On Snellius, submit:

``` bash
#!/bin/bash
#SBATCH -J scratch-node-test
#SBATCH -t 5
#SBATCH -p rome
#SBATCH --constraint=scratch-node

touch "$TMPDIR/testfile-scratch-node.foo"
echo "This is a file on scratch-node" > "$TMPDIR/testfile-scratch-node.foo"
realpath "$TMPDIR/testfile-scratch-node.foo"
```

On the course cluster, follow the tab: do not add `--constraint=scratch-node`. Keep the `touch`, the `echo`, and the `realpath`.

::: solution
## Solution

The output is one absolute path, and the path ends in `testfile-scratch-node.foo`.

On Snellius that path is on the node disk you requested. The directory is removed when the job ends, so the login node cannot open it afterwards. The line in the slurm output file is the record.

On the course cluster the constraint is absent. `realpath` still prints a path ending in `testfile-scratch-node.foo`, under the job's `$TMPDIR`. That directory is also removed when the job ends.

If the Snellius job waits and never starts, no node with the feature was free. Read the tab and the script, and do not drop the constraint on Snellius just to get a start. Drop it only on the machine whose tab says to drop it.
:::
::::::::::::

## A million to a billion values

`episodes/files/ex1/print-n.c` writes `n` random double-precision values to a file, in ASCII or in binary. It then prints how long the write took, the file size in MB, and the rate in MB/s. `run.sh` compiles it and calls it in a loop.

The script loads `module load 2025` and `GCC/14.2.0`, compiles `print-n.c` to `print-n.out`, and loops `i` from `ibeg` to `iend` (the end index is excluded). The defaults are `ibeg=6` and `iend=10`, so `n` is 10^6, 10^7, 10^8, and 10^9. The last array is 8 GB of memory. The file is ASCII, so it is larger than that array. `nmax` stops a run that would be even bigger.

`wdir` is the directory the file is written to. The default is `$HOME`. `wdir=TMPDIR` is a keyword. The script expands it to the job's `$TMPDIR` inside the job. Setting `wdir` to the login node's `$TMPDIR` before `sbatch` would point at the wrong directory. Use the keyword.

On Snellius, from the `ex1` directory:

``` bash
sbatch run.sh
```

That is the full run, 10^6 through 10^9 values, into home unless you set `wdir`. Remove `ex1.dat` when you have read the output. Home is 200 GiB. The file does not belong there overnight.

On a small cluster, do not submit the full range. The tab has the smaller command. The line for this exercise is:

``` bash
iend=8 wdir=TMPDIR sbatch run.sh
```

`iend=8` keeps `i` at 6 and 7, so the job writes 10^6 values and then 10^7 values, into the job's `$TMPDIR`. `iend=8 sbatch run.sh` writes those same two sizes into home, which is the comparison and also the one to avoid if home is tight. Prefer the `wdir=TMPDIR` form.

::: sites scale-two-core
:::

The other lines in that tab belong to later lessons. Use the `run.sh` line.

::: caution
## Do not fill home

The published default writes `ex1.dat` in home. On a small cluster, `iend=8 wdir=TMPDIR` keeps the file in the job directory, which is removed at the end of the job. The slurm output file in the submit directory is the part you keep. Delete a home copy if you made one.
:::

:::::::::::: challenge
## Run print-n at the size your machine can hold

From `episodes/files/ex1`, submit the full script on Snellius:

``` bash
sbatch run.sh
```

On a small cluster, submit the line from the tab:

``` bash
iend=8 wdir=TMPDIR sbatch run.sh
```

How many `Printing` lines do you get, and which powers of ten are they? Where is `ex1.dat`?

::: solution
## Solution

The program prints, for each `n`, a line of this shape, then the script prints `Printing`:

``` text
1000000 random double-precision values written to <path>/ex1.dat in ascii format
 Elapsed time [s]: <seconds>
 File size [MB]: <size>
 Transfer rate [MB/s]: <rate>
Printing 1000000 elements
```

The seconds, the size, and the rate depend on the node. ASCII is about 9 bytes per value (`0.123456` and a newline), so the 10^6 file is about 9 MB and the 10^7 file is about 90 MB. Do not expect those sizes to the last digit. Do expect the size to grow by about ten times when `n` grows by ten times.

On Snellius, `sbatch run.sh` prints four `Printing` lines: 1000000, 10000000, 100000000, and 1000000000. The default path is your home directory. Remove `ex1.dat` after you have read the rates.

On a small cluster, `iend=8 wdir=TMPDIR sbatch run.sh` prints two `Printing` lines: 1000000 and 10000000. The path contains the job's `$TMPDIR`. That directory is gone when the job ends. The slurm output file is still in the directory where you submitted.
:::
::::::::::::

::: instructor
## Optional

This challenge is optional. Skip it when time is short or when `df -h` shows little free space. On the course cluster, create 100 files of 1 MB, not 1000. If home and the scratch path are the same disk, the copy is not a useful comparison. Use the job's `$TMPDIR` as the destination, or skip the challenge.
:::

:::::::::::: challenge
## Optional: many small files against one archive

This is the cost from the first episode, timed.

On Snellius, create 1000 files of 1 MB in home, then copy them to scratch-shared. On the course cluster, create 100 files, and use the scratch path in the tab. Check `df -h` first. Stop if the free space is close to the size you are about to write.

::: sites scratch-places
:::

``` bash
mkdir ~/file_transfer_test
cd ~/file_transfer_test
for i in {1..1000}; do
  head -c 1M </dev/urandom > "file_${i}.bin"
done
du -sh ~/file_transfer_test
```

On the course cluster the loop is `{1..100}`.

Set `DEST` to `/scratch-shared/$USER` on Snellius, or to the scratch directory from the tab. Do not set `DEST` to `$TMPDIR` in this login shell. The login node's `$TMPDIR` is the wrong disk. On the course cluster, if you want the node disk, put the `cp` lines in a job and let that job expand `$TMPDIR`.

``` bash
time cp -r ~/file_transfer_test "$DEST/"
tar -C ~ -czf ~/file_transfer_test.tar.gz file_transfer_test
du -sh ~/file_transfer_test.tar.gz
time cp ~/file_transfer_test.tar.gz "$DEST/"
```

Then remove the test, in home and in `DEST`:

``` bash
rm -r ~/file_transfer_test
rm ~/file_transfer_test.tar.gz
rm -r "$DEST/file_transfer_test"
rm "$DEST/file_transfer_test.tar.gz"
```

Check `pwd` and `echo "$DEST"` before `rm -r`. Remove only this test.

What do you expect from the two `du` sizes, and which `time cp` finishes sooner?

::: solution
## Solution

`head -c 1M` writes 1,048,576 bytes. A thousand of those files is about 1000M. `du -sh ~/file_transfer_test` prints a size near `1000M` or `1.0G`. One hundred files, the course-cluster count, is near `100M`.

The archive is about the same size as the directory. The bytes are random. gzip does not compress them. The single file is the win, not a smaller file.

`time cp` of the archive finishes in less time than `time cp -r` of the loose files. The archive is one create and one stream of bytes. The directory is a thousand creates. That is the metadata server from the first episode.

After the four `rm` commands, `ls ~/file_transfer_test` fails because the directory is gone, and `ls "$DEST/file_transfer_test.tar.gz"` fails for the same reason. Home is back to the size it had before the test.
:::
::::::::::::

::: keypoints
- `$TMPDIR` in a job is that job's directory. Two jobs on `tcn386` got `scur1448.4401218` and `scur1448.4401219`.
- `realpath` on those jobs printed `/gpfs/scratch1/nodespecific/tcn386/` plus the same job directory.
- Scratch-node is `--constraint=scratch-node` on Snellius. The course cluster drops the constraint and uses `$TMPDIR`.
- `sbatch run.sh` writes 10^6 through 10^9 values. A small cluster uses `iend=8 wdir=TMPDIR sbatch run.sh`.
- A thousand small files copy slower than one archive of the same bytes. Clean the test up.
:::
