---
title: "Energy"
teaching: 10
exercises: 10
---

::: instructor
This episode is the first to cut.
:::

::: questions

- Which two Slurm lines turn on EAR monitoring?
- Which `eacct` columns are watts and joules?

:::

::: objectives

- Add `--ear=on` and `--ear-policy=monitoring` to a job.
- Read POWER (W) and ENERGY (J) from `eacct -j JOBID`.

:::

This episode is optional. It is the first one to drop if the room is short on time.

EAR is the Energy Aware Runtime on Snellius. The deck adds two lines to the job script:

```bash
#SBATCH --ear=on
#SBATCH --ear-policy=monitoring
```

and, in the script, the report switch:

```bash
export EARL_REPORT_LOOPS=1
```

Submit the job as usual. After it finishes:

```bash
eacct -j JOBID
```

Read POWER (W) and ENERGY (J). The SURF page for EAR is <https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/62226671/Energy+Aware+Runtime+EAR>.

The course cluster does not have this tool. Use the tab.

::: sites energy
:::

The deck's sample for job step `11041163-0` includes these fields: TIME(s) 56.64, POWER(W) 253.62, ENERGY(J) 14366. `253.62 * 56.64 = 14365.0368` J, which matches the ENERGY column to the nearest joule.

:::: challenge
## Which number is joules?

In that sample, which number is POWER and which is ENERGY? What are the units?

::: solution
## Solution

POWER (W) is 253.62 watts. ENERGY (J) is 14366 joules. 56.64 is TIME in seconds. On the course cluster, skip the live `eacct` job. The sample is enough to name the two columns.
:::
::::

::: keypoints

- `#SBATCH --ear=on` and `#SBATCH --ear-policy=monitoring` turn on EAR monitoring.
- `eacct -j JOBID` prints the report. Read POWER (W) and ENERGY (J).
- The deck's sample lists 253.62 W and 14366 J.
- This episode is optional, and it is the first to cut. The course tab says to skip the live job.

:::
