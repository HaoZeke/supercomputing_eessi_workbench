---
title: "Averages with a dependency"
teaching: 10
exercises: 25
---

::: questions

- Which version first makes the aggregation wait?
- Where in the job description do you read that?

:::

::: objectives

- Walk `qcg_job_v0.py` through `qcg_job_v4.py` in order.
- Point at `after=job_names` in `qcg_job_v1.py` as the first wait.
- Run one version at a time, with `QCG_MAX_INPUTS=100` and `--ntasks=2` on 2 cores.
- Convert the README's `CPUTimeRAW` of 7232 seconds to 2.0 SBU.

:::

## Same averages, one allocation

Example 4 repeats example 2 with QCG-PilotJob. One average per CSV, then one file `result.csv`. The inputs are the same NOAA daily files. Extract them with `tar -xvf input.tar.gz` in `episodes/files/hands-on/example_04`.

`qcg_job.sh` copies the submission directory to `$TMPDIR`, runs one Python file, and copies `result.csv` back to `results/`. It also archives the working directory to `results/log.<job id>.tar.gz`, excluding `input` and `result`.

The script as copied runs v1. The other versions are comments:

```bash
# execute jobs
# python3 qcg_job_v0.py
python3 qcg_job_v1.py
# python3 qcg_job_v2.py
# python3 qcg_job_v3.py
# python3 qcg_job_v4.py
```

Change which line is active, one version at a time. The Slurm header is one node, 16 tasks, 20 minutes, partition `rome`.

Every version reads `QCG_MAX_INPUTS`. `0`, which is the default in the Python, selects every CSV. Any other nonnegative value keeps that many files from the sorted list. On 2 cores the hands-on README uses 100 files:

```bash
QCG_MAX_INPUTS=100 sbatch --ntasks=2 qcg_job.sh
```

The `#SBATCH --ntasks=16` line stays in the file. `--ntasks=2` is the override.

## v0

`qcg_job_v0.py` builds one `Jobs` object. It adds an average job per CSV (`exec='python3'`, arguments `average.py` and the file, `iteration=1`). It then adds the aggregate in the same object:

```python
jobs.add(name="aggregate",
         script='cat average_*.csv | sort',
         stdout='result.csv',
         stderr='aggregate.err',
        )
```

There is no `after`. The aggregate is submitted together with the averages. Nothing in the description tells the manager to wait.

## v1

`qcg_job_v1.py` is the same list, and the aggregate gains one field:

```python
jobs.add(name="aggregate",
         script='cat average_*.csv | sort',
         stdout='result.csv',
         stderr='aggregate.err',
         after=job_names
        )
```

`job_names` is the list of average names. `after=job_names` is what makes the aggregation wait. This is the first version that has the field.

## v2

`qcg_job_v2.py` splits the work into `jobs_comp` and `jobs_agg`. It submits the averages, then waits on the ids the submit call returned:

```python
job_comp_ids = manager.submit(jobs_comp)
manager.wait4(job_comp_ids)
```

The comment above that call says you could use `manager.wait4all()` instead. The aggregate is a second submit, and it still sets `after=job_names`. The wait is now also in the Python, before that second submit. The field that first expressed the wait is still the one v1 added.

## v3

`qcg_job_v3.py` uses one `Jobs` object. It submits the averages, calls `manager.wait4all()`, then `jobs.clear()`, then adds the aggregate with `after=job_names` and submits that. Same wait, a third arrangement. The `after` field is still there.

## v4

`qcg_job_v4.py` is the version the README calls final. It waits in Python and checks each average before it submits anything for the aggregation:

```python
def succeeded(manager, ids):
    states = manager.status(ids)['jobs']
    return bool(ids) and all(states[name]['data']['status'] == 'SUCCEED' for name in ids)
```

```python
ids = manager.submit(jobs)
manager.wait4(ids)
if not succeeded(manager, ids):
    raise RuntimeError('An average task failed; aggregation cannot run')
```

The success state in that check is `SUCCEED`. The script writes the selected output names to `selected.json` under a `qcg-averages-*` directory. It then submits `aggregate.py` with that directory as the only argument. There is no `after` field on this aggregate. The wait already happened, and a failed average raises before the aggregate is submitted.

`aggregate.py` reads `selected.json`, requires one finite mean for each selected file, and writes sorted rows to stdout. The aggregate description sets `stdout='result.csv'`. `qcg_job.sh` copies that file to `results/`. The `qcg-averages-*` directory lives under the job's `$TMPDIR`, so it is gone after the job. The archive in `results/log.<job id>.tar.gz` is where the README says `selected.json` remains.

:::: challenge

## Which version first waits?

Open `qcg_job_v0.py` and `qcg_job_v1.py`. Which version first makes the aggregation wait, and which field says so?

::: solution

## Solution

v1. The aggregate description in `qcg_job_v1.py` is the first one that sets the field:

```python
         after=job_names
```

v0's `jobs.add` for `aggregate` has `script`, `stdout`, and `stderr`, and no `after`. v2 and v3 also set `after=job_names`. v4 waits with `manager.wait4` and the `SUCCEED` check, and its aggregate has no `after`. The first version is v1.

:::

::::

:::: challenge

## One version, 100 files

`qcg_job.sh` currently calls `qcg_job_v1.py`. On a 2-core node, what command runs 100 files? What do you change to run v0, and what do you change back before v4?

::: solution

## Solution

```bash
QCG_MAX_INPUTS=100 sbatch --ntasks=2 qcg_job.sh
```

To see v0, comment `python3 qcg_job_v1.py` and uncomment `python3 qcg_job_v0.py`. Restore a single active line before you move to v2, v3, or v4. `QCG_MAX_INPUTS=100` keeps the first 100 sorted names. `0` would select every CSV.

The README's accounting example, for a different job, is:

```text
sacct -X --format="JobID%24,Timelimit,AllocCPUS,CPUTime,CPUTimeRAW" -j 16235860
                   JobID  Timelimit  AllocCPUS    CPUTime CPUTimeRAW
------------------------ ---------- ---------- ---------- ----------
                16235860   00:20:00         16   02:00:32       7232
```

```text
1 SBU / CPU hour * 7232 CPU seconds / 3600 seconds per hour = 2.0
```

That 2.0 is the README's figure for job 16235860. Your job id, and your `CPUTimeRAW`, come from your own `sacct`.

:::

::::

::: keypoints

- v0 submits the aggregate with no `after`, so the description does not make it wait.
- v1 is the first version that waits. The field is `after=job_names`.
- v2 waits with `manager.wait4(job_comp_ids)`, v3 with `wait4all` and `jobs.clear()`. Both still set `after`.
- v4 checks status `SUCCEED`, writes `selected.json`, and only then submits `aggregate.py`.
- On 2 cores: `QCG_MAX_INPUTS=100 sbatch --ntasks=2 qcg_job.sh`.

:::
