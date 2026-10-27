---
site: sandpaper::sandpaper_site
---

This lesson moves data on a parallel file system. You pack small files, checksum the archive, resume a copy with `rsync`, and stage a tree onto the node disk for the length of a job.

One episode, on several streams and mpiFileUtils, is optional.

::: prereq

- [ ] You can open a terminal and run `tar`, `rsync`, and `sha256sum`
- [ ] You have a directory for a heavy copy. On a cluster, use scratch
- [ ] For the stage script, you can submit a Slurm job

:::
