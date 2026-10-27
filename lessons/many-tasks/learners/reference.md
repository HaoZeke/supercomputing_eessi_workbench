---
title: Glossary
---

QCG-PilotJob documentation: <https://qcg-pilotjob.readthedocs.io/en/develop/>.

Execution models: <https://qcg-pilotjob.readthedocs.io/en/develop/execution_models.html>.

Logs: <https://qcg-pilotjob.readthedocs.io/en/develop/logs.html>.

The deck's clone URL for the upstream course is <https://github.com/sara-nl/introduction-to-supercomputing>. This lesson already contains the hands-on tree.

Example 4's climate files are from the NOAA Global Historical Climatology Network daily product: <https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily>.

## Glossary

job array
: One Slurm submission of the same script, once per index.

SLURM_ARRAY_TASK_ID
: This task's array index.

SLURM_ARRAY_JOB_ID
: The first job ID of the array. In an output name, `%A` is replaced by it, and `%a` becomes the task index.

array throttle
: The `%` in `--array=0-10%2`. Slurm runs at most 2 of those tasks at once. `--array=0-10` is 11 tasks.

pilot job
: One Slurm allocation. A manager inside it starts the short tasks.

QCG-PilotJob
: The pilot manager in this lesson. A Python script describes the tasks. The Slurm script holds the allocation.

LocalManager
: The QCG object that uses the cores of the allocation you are already in.

after
: The field on a QCG job description that names tasks to wait for. `qcg_job_v1.py` is the first averages version that sets `after=job_names`.

HyperQueue
: A server and a worker inside the allocation. `hq submit --wait` returns when every submitted task has finished, and the aggregate command is the next line.

Snakemake
: Rules that name files. The aggregate rule waits because its `input` lists every average file.

FireWorks
: A LaunchPad of workflows. This lesson uses a file under `$TMPDIR` and one `rlaunch rapidfire` worker. The aggregate Firework sets `parents` to the average Fireworks.

system billing unit
: The deck's SBU. Example 4 converts `CPUTimeRAW` with `7232 / 3600 = 2.0` at 1 SBU per CPU hour, for job `16235860`.

idle time
: `1 - busy / (slots * span)` from the task lines. Span is `END - START`. Busy is the sum of the task durations.
