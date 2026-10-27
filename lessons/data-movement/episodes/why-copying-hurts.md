---
title: "Why copying hurts"
teaching: 10
exercises: 0
---

::: questions

- Why does a directory of small files copy slowly?
- Which directory is for the heavy copy, and which one exists only inside a job?

:::

::: objectives

- Separate the work of the data servers from the work of the metadata server.
- Put code in home, the heavy copy on scratch, long-lived group data on project, and node-disk files only inside a job.

:::

## A million small files

A parallel file system splits the work. **Data servers** move bytes. A **metadata server** records each create, open, and close. Copying a million small files asks that server for a million operations, and the data servers wait. Pack the files first.

Sam's case is the same shape at a smaller count. Thousands of output files, copied one by one, stall on metadata. The next episode packs 20,000 of them and times the difference.

## Where data lives

Keep code and notes in **home**. Do the heavy copy on **scratch**. Keep the group's long-lived data on the **project** file system. Use the **node disk** only inside a job. It is the fastest, and it disappears when the job ends.

The paths differ by machine.

::: sites scratch-places
:::

::: keypoints

- Data servers move bytes. The metadata server records create, open, and close.
- A million small files stall the copy. Pack them first.
- Home is for code, scratch is for the heavy copy, project is for long-lived group data.
- The node disk is only for the inside of a job.

:::
