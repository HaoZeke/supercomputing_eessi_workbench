---
title: "Other tools"
teaching: 20
exercises: 25
---

::: instructor

This episode is optional. Keep HyperQueue, Snakemake, and FireWorks. FireWorks is part of the comparison.

:::

::: questions

- Where does each tool say that the aggregation waits for every average?
- What is `measurements/sacct.txt` for, and what does it leave out?

:::

::: objectives

- Run the average and profile exercises with HyperQueue, Snakemake, and FireWorks.
- Read the HyperQueue `--wait`, the Snakemake aggregate `input`, and the FireWorks `parents`.
- Use 16 tasks for HyperQueue and Snakemake, and one worker for the file-backed FireWorks example.
- Read the 25 October 2026 table as one run, and use `sacct.txt` for the Slurm accounting of that run.

:::

## The same two exercises

`episodes/files/hands-on/alternatives/` repeats example 4 and example 5.

- Example 4: one average per CSV, then an aggregation that must wait for every average.
- Example 5: sleeps of different lengths, so idle time can be computed from each task's start and end.

HyperQueue and Snakemake request 16 tasks. The file-backed FireWorks example requests one task, for its one worker. The average scripts default to 100 files. `QCG_MAX_INPUTS=0` selects every file. Run each tool from its own directory. Two tools writing one `result.csv` in one directory will collide.

On 2 cores the README scales HyperQueue and Snakemake, and leaves FireWorks at one task:

```bash
QCG_MAX_INPUTS=100 sbatch --ntasks=2 average.sh
TIMES_FILE=../../example_05/times_short.txt sbatch --ntasks=2 profile.sh
```

FireWorks keeps `--ntasks=1`. For the short profile: `TIMES_FILE=../../example_05/times_short.txt sbatch profile.sh`.

The load line for each tool is the tab. The scripts also name a version.

::: sites hq-module
:::

::: sites snakemake-module
:::

::: sites fireworks-module
:::

::: sites scale-two-core
:::

## HyperQueue

A server and one worker run inside the allocation. The average script lists the CSV paths in `files.txt` and submits one task per line.

The dependency is `hq submit --wait`. The flag returns when every task has finished. The aggregation is the next line. From `alternatives/hyperqueue/average.sh`:

```bash
hq submit --each-line files.txt --cpus=1 --wait \
    --stdout "$averages/%{TASK_ID}.csv" --stderr "$averages/%{TASK_ID}.err" \
    -- bash -c 'python3 ../../example_04/average.py "$HQ_ENTRY"'

python3 ../aggregate.py "$averages"/*.csv > result.csv
```

The script loads `module load 2025`, `Python/3.13.1-GCCcore-14.2.0`, and `HyperQueue/0.24.0`. The alternatives README says `module spider HyperQueue` in the Snellius 2025 stack lists 0.19.0, 0.20.0, and 0.24.0, checked on 2026-10-25. The header asks for `--ntasks=16`.

`profile.sh` uses the same `--each-line` and `--wait` pattern on the times file, and prints `START` and `END` around that submit.

## Snakemake

`snakemake --cores "$SLURM_NTASKS"` runs the rules on the cores of the allocation. The average script's header also asks for `--ntasks=16`.

The dependency is the `input` of the aggregate rule in `alternatives/snakemake/Snakefile`:

```python
rule aggregate:
    input:
        expand("averages/{name}.csv", name=NAMES),
    output:
        "result.csv",
    shell:
        "cat {input:q} | sort > {output:q}"
```

Snakemake starts that rule when every file in the `input` list exists. `Snakefile.profile` has one `sleep` rule instance per line of the times file.

The alternatives README gives the module as `snakemake/9.22.0-foss-2025b`. It also says `module spider snakemake` finds nothing in the Snellius 2025 stack, and the script then activates `$HOME/venvs/snakemake`. The install line in that README is `pip install snakemake` after `module load 2025` and `Python/3.13.1-GCCcore-14.2.0`.

## FireWorks

FireWorks stores the workflow in a LaunchPad. Here the LaunchPad is a file under `$TMPDIR` (`MONGOMOCK_SERVERSTORE_FILE`). There is no MongoDB server. `rlaunch rapidfire` starts one worker, which runs each Firework that is ready until none remain.

A file LaunchPad allows one writer. The comment in `average.sh` says several `rlaunch` workers lose Firework states. The aggregate then never runs. Parallel workers need a MongoDB server. The header is one node and one task:

```bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:20:00
#SBATCH --partition=rome
```

`profile.sh` uses the same `--ntasks=1`. The tasks run one after another, because there is one worker.

The dependency is `parents=averages` on the aggregate Firework in `alternatives/fireworks/workflow.py`:

```python
command = shlex.join([sys.executable, os.path.join(HERE, "..", "aggregate.py"),
                      "--manifest", manifest])
aggregate = Firework(ScriptTask.from_str(f"{command} > {shlex.quote(os.path.join(HERE, 'result.csv'))}"),
                     name="aggregate", parents=averages)
lp.add_wf(Workflow(averages + [aggregate], name="average"))
```

`parents=averages` is the link. FireWorks runs that Firework after every average Firework has finished. The workflow writes `selected.json` and calls `aggregate.py --manifest`. HyperQueue still calls `aggregate.py` with the output paths as arguments.

The module line in the script is `FireWorks/2.1.4-gfbf-2025a`. The README says the Snellius 2025 stack has no FireWorks module, and the fallback is `$HOME/venvs/fireworks` with `pip install "fireworks[mongomock]"`.

On Snellius the one worker took 9 s for 100 files and 212 s for all 1000 files, on its one core. Snakemake took 15 s for the 1000 files on 16 cores, about 240 core-seconds. Per core those costs are close. The file LaunchPad still allows one worker, so FireWorks in this example cannot take more cores.

`average.sh` uses 100 of the 1000 files unless `QCG_MAX_INPUTS` says otherwise.

## One measured run

The slides and `alternatives/README.md` report one run on 25 October 2026: two-core nodes, each job alone, `--nodes=1 --ntasks=2` (FireWorks `--ntasks=1`), the 32 tasks of `times_short.txt` at their original lengths, 338 task-seconds in all. The slide says this is one run, and it is not a general result. A 16-core Snellius allocation was not measured for this table.

Idle is `1 - busy / (slots * span)`. Span is `END - START`. Busy is the sum of the task durations. The lanes in `plot_profile.py` are the CPU number a task reported when it started. Tasks are not pinned, so overlapping bars can leave white space in a lane. That white space is not the idle figure. The idle figure comes from the start and end times.

| Tool | Span | Idle | Where it sits |
| --- | --- | --- | --- |
| bash pipeline | 267 s | 37% | each block of 2 tasks waits for its longer task |
| QCG-PilotJob | 181 s | 7% | 1 s before the first task, 3 s after the last, short gaps |
| HyperQueue | 172 s | 2% | 1 s of start-up, 0.1 s between tasks |
| Snakemake | 250 s | 32% | 77 s of start-up before the first task; the tasks themselves spanned 171 s with 0.1 s gaps |
| FireWorks | 344 s | 2% of its one slot | one worker, so the tasks run one after another |

An earlier QCG run that loaded a module inside every task showed 23% idle. The examples pass no `modules=`, so a task inherits the job's environment and does not pay for a module load.

Averages of 100 files, same nodes:

| Tool | Time |
| --- | --- |
| HyperQueue | 11 s |
| QCG-PilotJob, `qcg_job_v4.py` | 18 s |
| FireWorks, one worker | 25 s |
| Snakemake | 67 s |

QCG's 7% is a second at the start and three at the end, plus short gaps. HyperQueue's 2% is the next task starting when a slot frees. Snakemake's gaps between tasks are the same 0.1 s. The 32% is the 77 s before the first task. FireWorks at 344 s is the one worker, task after task.

The bash pipeline's 37% is the block of 2: the block waits for its longer task. That is the same `wait` as in `pipeline.sh`.

## What sacct.txt is for

`episodes/files/hands-on/alternatives/measurements/sacct.txt` is the Slurm listing of that run. `measurements/README.md` says `measure.sh` submitted the nine jobs and `sacct.txt` lists them. The format in `measure.sh` is:

```bash
sacct -X -n -j "$ids" -o JobID,JobName%20,NodeList,AllocCPUS,Elapsed,State,ExitCode
```

The file has those nine lines:

```text
18158                 pipeline.sh     coursenode1          2   00:04:35  COMPLETED      0:0
18159                  qcg_job.sh     coursenode2          2   00:03:13  COMPLETED      0:0
18160                  profile.sh     coursenode3          2   00:03:04  COMPLETED      0:0
18161                  average.sh     coursenode3          2   00:00:11  COMPLETED      0:0
18162                  profile.sh     coursenode2          2   00:04:31  COMPLETED      0:0
18163                  average.sh     coursenode3          2   00:01:07  COMPLETED      0:0
18164                  profile.sh     coursenode3          1   00:05:57  COMPLETED      0:0
18165                  average.sh     coursenode3          1   00:00:25  COMPLETED      0:0
18166                  qcg_job.sh     coursenode1          2   00:00:18  COMPLETED      0:0
```

The output files next to it name the tool: `pipeline.18158.out`, `qcg.18159.out`, `hq.18160.out`, `hq-average.18161.out`, `snakemake.18162.out`, `snakemake-average.18163.out`, `fw.18164.out`, `fw-average.18165.out`, and `slurm-18166.out` for QCG-PilotJob v4 averages.

Elapsed is the scheduler column. The span in the idle table is `END - START` inside the job output. On the average jobs the two agree with the table (11 s, 67 s, 25 s, 18 s). On the profile jobs they differ. Job 18158's Elapsed is `00:04:35` and the pipeline span is 267 s. Use Elapsed when you want the accounting, and the span when you want the idle formula.

`sacct.txt` has no `CPUTimeRAW` column. The 2.0 SBU figure in example 4 is job `16235860`, not one of these nine. Core-hours for a new run use the example 4 format, `CPUTimeRAW / 3600`.

## How the deck chooses

- QCG-PilotJob and HyperQueue: many tasks inside one allocation. QCG-PilotJob is driven from Python. HyperQueue is driven from the command line, and it has a Python API as well.
- Snakemake: rules on files. A rerun builds what changed.
- FireWorks: a database of workflows, with states and reruns. Without a MongoDB server the file LaunchPad allows one worker.

:::: challenge

## Where the dependency is written

For the average exercise, name the line or field that makes the aggregation wait, in HyperQueue, in Snakemake, and in FireWorks.

::: solution

## Solution

HyperQueue: `hq submit --each-line files.txt --cpus=1 --wait` in `hyperqueue/average.sh`. The aggregate line is the `python3 ../aggregate.py` command after that submit returns.

Snakemake: the `input` of rule `aggregate` in `Snakefile`, `expand("averages/{name}.csv", name=NAMES)`.

FireWorks: `parents=averages` on the aggregate `Firework` in `fireworks/workflow.py`, in the `lp.add_wf(Workflow(averages + [aggregate], name="average"))` call.

QCG's first form of the same idea is `after=job_names` in `qcg_job_v1.py`.

:::

::::

:::::::::::: challenge

## Scale the optional run

You are on a 2-core node and you want the short profile from all three tools. What does FireWorks keep that the other two override? Which file lists the nine measured jobs?

::: sites scale-two-core
:::

::: sites hq-module
:::

::: sites snakemake-module
:::

::: sites fireworks-module
:::

::: solution

## Solution

HyperQueue and Snakemake take `--ntasks=2` on the command line. Their scripts still say `--ntasks=16`. FireWorks keeps `--ntasks=1`, because the file LaunchPad has one worker.

```bash
TIMES_FILE=../../example_05/times_short.txt sbatch --ntasks=2 profile.sh
TIMES_FILE=../../example_05/times_short.txt sbatch profile.sh
```

The second line is the FireWorks directory. The first is HyperQueue or Snakemake, from that tool's directory.

`episodes/files/hands-on/alternatives/measurements/sacct.txt` lists the nine jobs from 25 October 2026: job id, name, node, allocated CPUs, Elapsed, state, and exit code. The idle percentages are computed from `START`, `END`, and `TASK` lines, not from the Elapsed column.

:::

::::::::::::

::: keypoints

- HyperQueue waits with `hq submit --wait`. The aggregate command is the next line.
- Snakemake waits because the aggregate rule's `input` lists every average file.
- FireWorks waits with `parents=averages`. The file LaunchPad has one worker and the script asks for one task.
- HyperQueue and Snakemake scripts request 16 tasks. On 2 cores, override with `--ntasks=2`.
- The 25 October 2026 table is one run: pipeline 267 s and 37% idle, QCG 181 s and 7%, HyperQueue 172 s and 2%, Snakemake 250 s and 32%, FireWorks 344 s and 2% of one slot.
- `measurements/sacct.txt` is the Slurm accounting for that run. It has Elapsed, and it has no `CPUTimeRAW`.

:::
