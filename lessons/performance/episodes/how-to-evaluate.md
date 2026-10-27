---
title: "How to evaluate a run"
teaching: 15
exercises: 5
---

::: questions

- What do you do after a run finishes, and what do you do with that answer?
- Which line of `time -p` is the time you waited?

:::

::: objectives

- Name the three steps in the life cycle of an HPC application.
- Time one short command with `time -p` and read `real`.

:::

## The life cycle

An HPC application is software written to use a supercomputer or a cluster on a hard problem. It does three kinds of work: intensive computation, communication between parallel processes, and input and output on a fast file system.

The life cycle is a loop with three steps.

1. Run the application.
2. Evaluate the performance.
3. Make changes to the application.

Then you run it again. A change you have not timed is a guess.

## What "evaluate" can mean

The deck lists several ways to evaluate a run:

- Tools such as Score-P, Scalasca, Nsight Systems, and AMD uProf.
- The execution time.
- The memory footprint.
- The network load.
- A comparison with a similar application or model.
- A comparison on different hardware.
- A guess you have not measured.

This episode uses the second one. You time one short command and write down a single number. Later episodes compare that kind of number. They do not replace this first step.

## `time -p`

`time -p` is the POSIX form. It prints three lines on standard error.

- `real` is the elapsed time, the seconds you waited. That is the wall-clock time.
- `user` and `sys` are CPU time. Added together they can be larger than `real` when several cores run at once. They can be near zero when the process is waiting.

:::: challenge
## One short timed run

Run:

```bash
time -p sleep 1
```

Which line is the wall-clock time, and about how large is it?

::: solution
## Solution

`real` is the wall-clock time. For `sleep 1` it is about 1 second. `user` and `sys` are near zero because the process spent the second waiting, not computing. Write the `real` line down. That is the whole measurement this episode asks for: one short timed run, one number.
:::
::::

::: keypoints

- The life cycle is run, evaluate, change, and run again.
- `time -p` prints `real`, `user`, and `sys`.
- `real` is the wall-clock seconds you waited.
- Start with one short timed run before you reach for a profiler.

:::
