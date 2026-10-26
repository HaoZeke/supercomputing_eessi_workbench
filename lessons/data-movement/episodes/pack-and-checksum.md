---
title: "Pack, then checksum"
teaching: 10
exercises: 15
---

::: questions

- Why is one archive faster to copy than the directory it came from?
- What does `sha256sum -c` print when the archive still matches?

:::

::: objectives

- Build a tar archive with `--sort=name` and a squashfs image with `mksquashfs -comp zstd`.
- Time `cp -r`, tar then `cp`, and `rsync -a` on 20,000 small files.
- Check the archive after the copy and read `src.tar: OK`.

:::

## One archive, then a checksum

Turn a directory of small files into one archive, then record a checksum. Check it again after the copy. A squashfs image is one file you can mount read-only.

GNU tar, `sha256sum`, and `mksquashfs` are the tools. `--sort=name` makes the tar bytes stable from one run to the next.

```bash
tar --sort=name -cf run.tar run/
sha256sum run.tar > run.tar.sha256
sha256sum -c run.tar.sha256
mksquashfs run run.sqfs -comp zstd
```

`sha256sum -c` reads the `.sha256` file and prints the archive name and `OK` when the bytes match. The hands-on below uses `src.tar`, and that check prints `src.tar: OK`.

## Write the order first

Use bash. `time` prints real, user, and sys. Write down real.

The deck's sequence is `episodes/files/predict.sh`. Run it from an empty directory on scratch, so the 20,000 files stay off home.

```bash
mkdir -p src out
yes data | head -n 20000 | split -l 1 -a 5 -d - src/f
ls src | wc -l
{ time cp -r src out/by-cp; }
tar --sort=name -cf src.tar src
{ time cp src.tar out/; }
{ time rsync -a src/ out/by-rsync/; }
sha256sum src.tar > src.tar.sha256
cp src.tar.sha256 out/
( cd out && sha256sum -c src.tar.sha256 )
```

`yes data | head -n 20000 | split -l 1 -a 5 -d - src/f` writes 20,000 files. Each file is one line. The suffixes from `-a 5 -d` run from `f00000` through `f19999`. `ls src | wc -l` prints 20000.

`cp -r` creates 20,000 files at the destination. `rsync -a` does the same. `tar --sort=name -cf src.tar src` builds one archive, and `cp src.tar` moves that one file. The metadata server does one create for the tar copy, and 20,000 creates for each of the other two.

:::: challenge

## Predict the order

Before you run the script, write the order of the three real times. Which copy is fastest, and why?

::: solution

## Solution

Tar then `cp` is fastest because it moves one file. `cp -r` and `rsync -a` each create 20,000 files.

A reference run on a local ext4 disk, 26 October 2026, matched that order. Record your own seconds. The deck does not list the three real times from that run. After the copy, `sha256sum -c` prints `src.tar: OK`.

:::

::::

:::: challenge

## Time it and check the archive

Change to an empty directory on scratch, then run `bash` on `episodes/files/predict.sh` from this lesson. Write down the three real times, and write down the `sha256sum -c` line.

::: solution

## Solution

The file count line is 20000. The real time for `cp src.tar` is the smallest of the three, because that copy is one file. `cp -r` and `rsync -a` each create 20,000 files, so they take longer. The check line is:

```text
src.tar: OK
```

Your seconds will differ from the ext4 run on 26 October 2026. The order is the result to compare.

:::

::::

::: keypoints

- `--sort=name` keeps the tar bytes stable from one run to the next.
- `mksquashfs run run.sqfs -comp zstd` packs the directory into one mountable file.
- On 20,000 small files, tar then `cp` is fastest because it moves one file.
- `sha256sum -c` prints `src.tar: OK` when the copied archive matches.

:::
