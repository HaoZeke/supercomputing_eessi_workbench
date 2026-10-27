---
title: "rsync"
teaching: 10
exercises: 15
---

::: questions

- Which flags let a stopped copy continue?
- What does `cmp` print when the two files match?

:::

::: objectives

- Copy with `rsync -a --partial` and read one progress line from `--info=progress2`.
- Use a trailing slash on the source so the contents arrive, with no extra directory level.
- Stop one `rsync` with `timeout`, run it again, and check the bytes with `cmp`.

:::

## One careful copy

`-a` keeps links, times, and permissions. `--partial` leaves a broken file in place so the next run continues. `--info=progress2` is one progress line for the whole transfer. `--checksum` reads every byte when size and time are not enough. A trailing slash on the source copies the contents, and it does not add an extra directory level.

Resume by running the same command again:

```bash
rsync -a --partial \
  --info=progress2 \
  run/ /scratch-shared/$USER/run/
```

When size and time are not enough, add `--checksum`:

```bash
rsync -a --checksum --partial \
  run/ /scratch-shared/$USER/run/
```

`run/` with the slash fills `/scratch-shared/$USER/run/` with the contents of `run`. The same source without the slash copies the directory as well, so the files sit at `run/run/`.

## Catch it midway

Predict a short `part/big.bin` after `timeout`, then equal sizes. `--bwlimit` slows the first copy so two seconds is enough to stop it. `--partial` keeps the broken file, and the next `rsync` continues.

`cmp` exits 0 when the bytes match, and it prints nothing.

`dd` with `bs=1M count=48` writes 48 MiB, which is 50331648 bytes. That is the size of `big.bin`. The partial file is shorter. On the ext4 example from 26 October 2026 it was 4128768 bytes of 50331648. Your byte count after two seconds can differ. The check is that the first `ls` shows a short file, the second `rsync` finishes the copy, and `cmp` is silent.

```bash
dd if=/dev/zero of=big.bin bs=1M count=48
mkdir -p part
timeout 2 rsync -a --partial \
  --bwlimit=2000 big.bin part/
ls -l big.bin part/big.bin
rsync -a --partial big.bin part/
cmp big.bin part/big.bin
```

`timeout` stops the first `rsync`. That line is the interrupted copy. Continue with `ls`.

:::: challenge

## Predict the two sizes

You run the block above. After `timeout`, how does `part/big.bin` compare with `big.bin`? After the second `rsync`, what does `cmp` print, and what is its exit status?

::: solution

## Solution

After `timeout`, `part/big.bin` is shorter than `big.bin`. `big.bin` is 50331648 bytes. On the ext4 run of 26 October 2026 the partial file was 4128768 bytes. After the second `rsync` the sizes match. `cmp big.bin part/big.bin` prints nothing and exits 0.

:::

::::

:::: challenge

## Resume it

In an empty directory, run the six commands from this episode. Record the two sizes from the first `ls -l`, then run `cmp` and record its exit status with `echo $?`.

::: solution

## Solution

The first size column for `part/big.bin` is smaller than 50331648. The ext4 reference is 4128768 bytes. The second `rsync` makes the sizes equal. `cmp` prints nothing. `echo $?` prints 0.

:::

::::

::: keypoints

- `-a` keeps links, times, and permissions. `--partial` keeps a broken file for the next run.
- `--info=progress2` is one progress line. `--checksum` reads every byte.
- A trailing slash on the source copies the contents.
- `timeout 2` with `--bwlimit=2000` leaves a short `part/big.bin`. The next `rsync` finishes it.
- `cmp` prints nothing and exits 0 when the bytes match.

:::
