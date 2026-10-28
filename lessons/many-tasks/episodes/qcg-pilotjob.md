---
title: "QCG-PilotJob"
teaching: 25
exercises: 20
---

::: questions

- What does QCG-PilotJob keep, while it runs many short tasks?
- Which lines in `qcg_job.py` and `qcg_job.sh` submit 512 `hostname` tasks?

:::

::: objectives

- Describe QCG-PilotJob as a manager inside one Slurm allocation.
- Read the Slurm script, the Python script, the job-description fields, and the execution models.
- Predict the two lines `qcg-three.py` prints.
- Run example 3: 512 tasks, two full `rome` nodes, the `default` model, 256 tasks on each node.

:::

## A manager inside the allocation

QCG-PilotJob submits jobs inside one large allocation, including an allocation that spans nodes. It does not take a fresh small allocation for each task the way an array does. It places each job onto the cores that job asked for, so the allocation stays full. Failed or timed-out jobs can be restarted. You can also set dependencies from results.

The costs are concrete.

- You estimate the total time of all the jobs combined, because the Slurm job has one time limit.
- Job and service state files appear in the submission directory.
- A Singularity container that embeds an MPI program gets harder to launch.
- When something fails, the log files may say little.

The path is three files. The Slurm script describes the resources, loads QCG-PilotJob, and runs the Python script. The Python script builds a manager and the job list. The executable is the program those jobs run.

Documentation: <https://qcg-pilotjob.readthedocs.io/en/develop/>.

## The Slurm script

Load the real QCG-PilotJob installation from the course CernVM-FS repository. Initialize EESSI 2025.06, add the site module directory and load the exact module below inside the batch script. The year aliases are compatibility names; they do not install QCG-PilotJob.

The deck's smallest script is one node, 16 cores, partition `rome`, ten minutes, then:

```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module use /cvmfs/course.surf-src.cvmfs/eessi/versions/2025.06/software/linux/x86_64/amd/zen2/modules/all
module load QCG-PilotJob/0.14.1-GCCcore-14.2.0
python test.py
```

Example 3's `episodes/files/hands-on/example_03/qcg_job.sh` is the script you submit for the 512 tasks. These are the lines in the file:

```bash
#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --time=00:05:00
#SBATCH --partition=rome

# QCG-PilotJob is installed in the 2024 stack only (toolchain gfbf-2024a)
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module use /cvmfs/course.surf-src.cvmfs/eessi/versions/2025.06/software/linux/x86_64/amd/zen2/modules/all
module load QCG-PilotJob/0.14.1-GCCcore-14.2.0

python3 qcg_job.py
```

Two nodes, 128 tasks per node, five minutes, partition `rome`. The comment in the file is the toolchain note. Leave those lines as published.

::: sites qcg-modules
:::

::: sites partition-request
:::

::: sites cpu-minimum
:::

The hands-on README's example for a small node, after you have checked `sinfo -o '%n %c'`, is:

```bash
sbatch --nodes=3 --ntasks-per-node=2 qcg_job.sh
```

That override is for this example's full-node request. The 16-core and 28 GiB minimum from the array episode is the deck's Snellius floor on `rome`. Example 3 asks for a full node of 128 cores, which is above that floor. The cpu-minimum tab is the floor on the machine in your welcome note.

## The Python script

The deck's minimal script creates a manager, prints the resources, waits, and finishes:

```python
from qcg.pilotjob.api.manager import LocalManager
manager = LocalManager()
print('available resources: ', manager.resources())
manager.wait4all()
manager.finish()
```

The slide's example output is for the 16-core script (`#SBATCH -n 16`):

```text
available resources: {'total_nodes': 1, 'total_cores': 16, 'used_cores': 0, 'free_cores': 16}
```

That dict is the slide's example for 16 cores. Example 3 does not print `resources()`, and its allocation is the two-node script above.

Working with the manager has three steps. Create it. Wait until the jobs you submitted have finished (`wait4all`, or `wait4` on a list of ids). Call `finish()`, which stops the background thread the manager runs in.

To run several programs you create a `Jobs` object, add descriptions, and `submit` that object:

```python
from qcg.pilotjob.api.job import Jobs
jobs = Jobs()
jobs.add(...)
jobs_ids = manager.submit(jobs)
```

## Fields and execution models

The deck's main fields:

- `name`, the job name
- `exec`, the path to the executable
- `args`, the arguments
- `script`, bash to run when you are not pointing at an executable
- `stdin`, `stdout`, `stderr`, the three files
- `modules`, modules to load before that job starts
- `numCores`, how many cores
- `numNodes`, how many nodes
- `iteration`, how the description repeats
- `model`, how the processes start

Execution models, from the same deck:

- `default` launches a single process in the allocation it was given
- `threads` is for OpenMP on one node
- `openmpi` starts the processes with `mpirun`
- `intelmpi` is the Intel MPI form
- `srunmpi` starts the processes with `srun`

More on the models: <https://qcg-pilotjob.readthedocs.io/en/develop/execution_models.html>.

The deck's executable example uses `script` and `iteration` instead of `exec`. Four iterations, one description:

```python
from qcg.pilotjob.api.manager import LocalManager
from qcg.pilotjob.api.job import Jobs

manager = LocalManager()
jobs = Jobs()
jobs.add(script='echo "job ${it} executed at `date` @ `hostname`"',
         name='test_job',
         stdout='job.out.${it}',
         iteration=4)
job_names = manager.submit(jobs)
print('submited job names: ', str(job_names))
job_status = manager.status(job_names)
print('job status: ', job_status)
manager.wait4all()
manager.finish()
```

The print text on the slide is `submited`, with that spelling. The date and the hostname in `job.out.${it}` depend on the node and the clock. This episode does not ask you to predict them. The next challenge is a different file, with three tasks and a fixed line.

:::: challenge

## Predict the printed line

Read `episodes/files/exercises/qcg-three.py`. The loop is `for i in range(3)`. Each task runs `/usr/bin/printf` with the argument `task-<i>\n` and writes `out_<i>.txt`. The script then does this:

```python
print("qcg-finished")
print(open("out_0.txt", encoding="utf-8").read().strip())
```

What two lines does the script print?

::: solution

## Solution

```text
qcg-finished
task-0
```

`printf` receives the format `task-0\n` for the first task, so `out_0.txt` holds `task-0` and a newline. `strip()` removes the newline. The script prints `out_0.txt` only. `task-1` and `task-2` stay in `out_1.txt` and `out_2.txt`. The task names in the description are `job_0`, `job_1`, and `job_2`.

The script changes to a temporary directory before it submits, so those files are not left in the lesson tree. The two lines above are what the source prints. They do not depend on a hostname.

:::

::::

## Example 3: 512 hostname tasks

The task is 512 independent short jobs on two nodes of the `rome` partition. The hands-on text says each node in that partition has 128 cores. Use `hostname` as the executable and `default` as the model.

`episodes/files/hands-on/example_03/qcg_job.py` is the description. The lines that create the tasks:

```python
# create 512 independent jobs
for job in range(512):
    # define a job
    jobs.add(name="job_{}".format(job),
             exec='hostname',
             stdout='output/job.{}.out'.format(job),
             stderr='output/job.{}.err'.format(job),
             model='default',
             numCores={ "exact" : 1},
             iteration=1)
```

`numCores={ "exact" : 1}` is one core. `model='default'` is one process. `iteration=1` runs the description once per name. The names are `job_0` through `job_511`.

The script then submits and waits. These are the print lines in the file:

```python
print("-- submit jobs")
manager.submit(jobs)
print("-- wait for all jobs")
manager.wait4all()
manager.finish()
print("-- finished")
```

Two nodes of 128 cores give 256 cores. Each task takes one core, and there are 512 tasks, so each node runs 256 tasks. Each task writes one line, the hostname, into `output/job.<n>.out`. Counted across those files, each node name appears in 256 lines.

The hands-on README says the state of each job is in `nl-agent-{hostname}.log`. The log page is <https://qcg-pilotjob.readthedocs.io/en/develop/logs.html>. This lesson has no sample of that log, so the states to read are the ones in the file you get after the run.

The Python creates `output/` (`os.makedirs("output", exist_ok=True)`). Later examples remove `.qcgpjm-service*` and `.*:0.hostfile`. Those are the service files the cleanup script knows about. The slide also says state files appear in the submission directory.

:::::::::::: challenge

## 256 lines, and the files you submit

From `example_03`, name the node count, the tasks per node, and the number of `hostname` tasks. How many of those tasks run on each node?

Submit the published `qcg_job.sh`. If `sinfo` shows fewer cores than 128, use the README's override and the tabs. Leave the script body as it is.

::: sites qcg-modules
:::

::: sites partition-request
:::

::: sites cpu-minimum
:::

::: solution

## Solution

`qcg_job.sh` requests `--nodes=2`, `--ntasks-per-node=128`, `--partition=rome`, and `--time=00:05:00`. `qcg_job.py` adds 512 jobs with `exec='hostname'`, `model='default'`, and `numCores={ "exact" : 1}`.

256 tasks run on each node: 512 tasks, two nodes, one core each, 128 cores on the node the hands-on describes. Each output file is one hostname line, so each node name accounts for 256 lines.

The small-node override from the hands-on README is `sbatch --nodes=3 --ntasks-per-node=2 qcg_job.sh`, after `sinfo`. The tabs are the load line, the partition, and the core floor for this machine. The module lines and the partition line inside the script stay as published.

A finished Python script prints:

```text
-- submit jobs
-- wait for all jobs
-- finished
```

The hostnames are the contents of `output/job.*.out`, not those three lines.

:::

::::::::::::

::: keypoints

- QCG-PilotJob is a manager inside one Slurm allocation. The Slurm script loads it and runs the Python script.
- The published example 3 script loads `2024` and `QCG-PilotJob/0.14.1-GCCcore-14.2.0`, and asks for 2 nodes at 128 tasks per node on `rome`.
- `qcg-three.py` prints `qcg-finished` and then `task-0`.
- Example 3 runs 512 `hostname` tasks, `model='default'`, one core each. That is 256 tasks on each of the two nodes.
- Job states are in `nl-agent-{hostname}.log`.

:::
