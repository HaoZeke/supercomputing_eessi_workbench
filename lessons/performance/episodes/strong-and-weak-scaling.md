---
title: "Strong and weak scaling"
teaching: 15
exercises: 20
---

::: questions

- What stays fixed in strong scaling, and what grows in weak scaling?
- How do you get an efficiency of 0.625 from 8.0 seconds and 1.6 seconds?

:::

::: objectives

- Define strong scaling, weak scaling, speedup, and efficiency.
- Compute the worked 8-core efficiency 0.625.
- Design a strong AXPY series and a weak AXPY series without copying `axpy.c`.

:::

## Two definitions

Strong scaling keeps the problem size fixed and increases the number of processors. The hope is that the same work finishes sooner. Amdahl's law says the serial share caps that hope. If `s` is the fraction of the time that stays serial, `p` is the parallel share, and `N` is the number of processes, then:

```text
speedup = 1 / (s + p/N)
```

Weak scaling increases the problem size with the number of processes. Each process keeps about the same amount of work. Gustafson's law says the parallel part grows with the resources and the serial part stays fixed as the problem grows:

```text
speedup = s + p*N
```

In both laws, `s` is the serial share of the time and `p` is the parallel share. `N` is the number of processes.

Measured speedup and efficiency use the times you record. `T_s` is the serial time. `T_N` is the time on N processes.

```text
speedup = T_s / T_N
efficiency = T_s / (N * T_N)
```

An efficiency of 1 would mean every added process carried a full share of the time. Communication, startup, and the serial share pull the number down.

## A worked efficiency

This table is a worked strong-scaling series from the timing material in this course. The problem size stays fixed. The efficiencies are 1.000, 0.909, 0.800, and 0.625. The series is a worked example. Record AXPY on its own.

| Cores | Seconds | Speedup | Efficiency |
| --- | --- | --- | --- |
| 1 | 8.0 | 1.000 | 1.000 |
| 2 | 4.4 | 1.818 | 0.909 |
| 4 | 2.5 | 3.200 | 0.800 |
| 8 | 1.6 | 5.000 | 0.625 |

Eight cores finish in 1.6 seconds. One core takes 8.0 seconds. The speedup is `8.0 / 1.6 = 5`. The efficiency is `8.0 / (8 * 1.6) = 8.0 / 12.8 = 0.625`. The extra cores helped, and they helped less than the first ones.

## AXPY, strong and weak

The binary is the hybrid AXPY in the hybrid MPI and OpenMP lesson: <https://supersurf.rgoswami.me/hybrid-jobs/>. The source there is `episodes/files/hands-on/ex2/axpy-hybrid.c`, built by `submit-axpy-hybrid.sh` as `axpy-hybrid.out`. Do not paste a second copy of that program here.

AXPY is `y = a * x + y` on a vector of length `n`. The hybrid program splits `n` across tasks. It is pointwise and limited by memory bandwidth.

Strong scaling: keep `n` fixed and run 1, 2, 4, and 8 tasks. You are asking the same bytes to finish sooner.

Weak scaling: multiply `n` by the task count, so each task's local length stays about the same. One task at length `n`, two tasks at length `2n`, four at `4n`, eight at `8n`.

Weak scaling stays flatter. Each task still moves about the same number of bytes, so the time stays nearer the one-task time. Strong scaling of this kernel drops and then flattens, because the bytes still have to move and the memory path fills up. This episode does not include a measured AXPY table. The shape is the point. The hybrid lesson is where you record the times.

A two-core node cannot hold eight tasks at one core each. Pass a smaller request on the `sbatch` command line. The tab says how, and it says to check `sinfo` first.

::: sites scale-two-core
:::

:::: challenge
## Efficiency, then two AXPY plans

The table says 8.0 seconds on 1 core and 2.5 seconds on 4 cores. What is `8.0 / (4 * 2.5)`?

Then write two command plans for the hybrid AXPY, using task counts 1, 2, 4, and 8. In the strong plan, what happens to `n`? In the weak plan, what happens to `n`? Which series should stay flatter, and why?

::: solution
## Solution

`8.0 / (4 * 2.5) = 8.0 / 10 = 0.8`. The table rounds that efficiency to 0.800. The speedup on that row is `8.0 / 2.5 = 3.2`.

Strong plan: one fixed `n`, and `--ntasks` of 1, then 2, then 4, then 8, with one core per task. The global vector does not change.

Weak plan: the same task counts, and `n` scaled by the task count. If the one-task length is `n`, the eight-task length is `8n`. Each task's local length stays near `n`.

The weak series stays flatter. AXPY's time follows the bytes each task moves. Strong scaling keeps the global bytes fixed and splits them, until bandwidth stops the split from helping. Weak scaling gives each task a similar vector, so the time stays nearer the one-task time.

On a two-core node, 4 and 8 tasks do not fit on one node. The tab is the rule for passing a smaller request. Check `sinfo` before you copy a core count. The 0.625 row is the worked table above. Your AXPY times are a separate measurement.
:::
::::

::: keypoints

- Strong scaling fixes the problem size. Weak scaling grows it with the processes.
- Amdahl: `1 / (s + p/N)`. Gustafson: `s + p*N`.
- Speedup is `T_s / T_N`. Efficiency is `T_s / (N * T_N)`.
- `8.0 / (8 * 1.6) = 0.625` on the worked 8-core row.
- For AXPY, fixed `n` at 1, 2, 4, and 8 tasks is strong scaling. `n` scaled by the task count is weak scaling, and that series stays flatter.

:::
