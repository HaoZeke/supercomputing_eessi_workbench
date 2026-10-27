# Instructors

The course has three sessions of four hours. Part I is the Introduction to HPC session: fundamentals, EESSI and first batch jobs. Use the running order below for that class. The full episode timings are reference estimates for teaching each complete lesson; do not add them together as the Part I timetable.

## Part I: exactly four hours

Times are elapsed from the start. Add the room's start time. This plan includes a 15-minute break and a final ten-minute recovery and exit-check block. Learners need a terminal, their own course account and the [setup page](/setup.html).

### 00:00-00:10 (10 min): purpose and destination.

Fundamentals slides pages 1-5; [Why use a cluster?](/fundamentals/10-hpc-intro.html). Explain the goal: submit a correct job, retain its output and explain its resource request. Ask for one task from the room that needs more memory, arithmetic or independent runs.
### 00:10-00:35 (25 min): access and shell.

Slides pages 22-26; [Connecting](/fundamentals/11-connecting.html). Spend ten minutes signing in and fifteen on `whoami`, `pwd`, `hostname` and a private working directory. Check that every pair can open a shell. Pair a learner with an access problem while the instructor handles the account privately.
### 00:35-00:55 (20 min): nodes, processes and cores.

Slides pages 6-17; [Exploring the cluster](/fundamentals/12-cluster.html). Explain login versus compute nodes, then ask pairs to locate their current host and read `sinfo`. A node allocation does not make a serial program parallel.
### 00:55-01:25 (30 min): EESSI and modules.

Slides pages 27-30 and 40-45; [Shared stack](/eessi/shared-stack.html) and [Finding modules](/eessi/finding-modules.html). Use fifteen minutes to explain and fifteen to purge, load the course stack and record Python's version and `module list`. Keep the course-cluster tab selected. The client-container episode is a fallback reading, not an image download during class.
### 01:25-01:55 (30 min): first batch job.

Slides pages 31-39 and 46-48; [Scheduling jobs](/fundamentals/13-scheduler.html) and [Python and OpenMP](/fundamentals/python-and-openmp.html). Explain the script for ten minutes and allow twenty for the Python submission, queue inspection and output. Submit `python.sh` from its hands-on directory. The output must contain `sum: 499999500000`. Save the job ID. Use the script's Python module version; it differs from the module discovery example.
### 01:55-02:10 (15 min): break.

Leave the return time visible. A pending job may finish during the break. Do not submit a second copy because the first is pending.
### 02:10-02:40 (30 min): requests and accounting.

Slides pages 11-21 and 34-39; [Accounting on Snellius](/fundamentals/surf-accounting.html) and [Resources](/fundamentals/18-resources.html). Give fifteen minutes of explanation and fifteen for pairs to calculate 16 cores for two hours on Snellius rome: 32 SBU. Explain the 16-core minimum there and the course cluster's smaller CPU request. SRC workspace credits and job SBU are different accounting systems.
### 02:40-03:20 (40 min): one node, one or two threads.

Slides pages 46-48; [Python and OpenMP](/fundamentals/python-and-openmp.html). Explain processes versus threads for ten minutes; give twenty for compilation and the two-CPU job, then ten to compare the two results. Use `sbatch --cpus-per-task=2 pi.sh`. Expect two `pi = 3.141592654` lines, with threads 1 and 2. Timing may differ; correctness must agree. The compiler step belongs in an allocation as shown below.
### 03:20-03:40 (20 min): independent work and arrays.

QCG deck pages 1-13; [Job arrays](/fundamentals/21-array.html). Explain an array for ten minutes and spend ten reading its index and concurrency limit. Submit only the small classroom example below. Do not run the 100-input comparison or install workflow tools in Part I.
### 03:40-03:50 (10 min): keep the result.

Fundamentals slides pages 18-21; [Transferring files](/fundamentals/16-transferring-files.html). Ask each pair to choose a durable location for the job script and output. Distinguish home/project, shared scratch and node-local temporary files. The detailed filesystem and transfer lessons belong to Part II.
### 03:50-04:00 (10 min): exit check and recovery margin.

Each pair shows a job ID, the sum, the two pi lines, the loaded environment and the output location. Ask what it requested and where it ran. This block also absorbs short queue and access delays. Keep the break and the first successful job; shorten the array discussion if the room needs more help.

## Instructor pack

Keep the [teacher workbook](/downloads/intro-teacher-workbook.pdf) on a separate screen. The [matching slide pack](/downloads/introduction-slides.zip) contains the concise controller lesson and the audited extended decks. Page references above refer to the PDF pages in that pack. The workbook provides extended explanations, worked answers, misconceptions and recovery guidance. Its storage, workflow and performance chapters are references for Parts II and III, not additional Part I requirements.

The learner website is a Carpentries Workbench lesson, not a remote desktop or a computing allocation. Open the course portal from the private welcome note in a separate tab. Keep the roster, MFA setup and individual enrollment URLs off the projector.

## Runnable source and commands

The website's exercise files are in a separate checkout from `~/introduction-to-supercomputing`. Clone once; inspect an existing directory instead of cloning over it.

```bash
git clone https://github.com/HaoZeke/supercomputing_eessi_workbench.git "$HOME/supercomputing_eessi_workbench"
cd "$HOME/supercomputing_eessi_workbench/lessons/fundamentals/episodes/files/hands-on"
sbatch --partition=rome --cpus-per-task=1 python.sh
squeue -u "$USER"
```

Read `slurm-JOBID.out` using the job ID that `sbatch` returns. The first line names the allocated host and the sum line is `sum: 499999500000`. These files match the published fundamentals hands-on examples. Keep `#SBATCH --partition=rome` in the scripts and use command-line overrides for the classroom request.

Compile within a small allocation, then submit the published OpenMP script:

```bash
srun --partition=rome --ntasks=1 --cpus-per-task=2 --time=00:05:00 bash compilepi
sbatch --partition=rome --cpus-per-task=2 pi.sh
```

The published script requests 32 CPUs, so the two-CPU override matters. Read the output only when the job has finished. It must report the same nine decimal digits for one and two threads. Do not promise that this short loop scales well.

For the array discussion, from your own working directory:

```bash
sbatch --partition=rome --ntasks=1 --cpus-per-task=1 --time=00:02:00 \
  --array=0-3%2 --output='intro-array-%A_%a.out' \
  --wrap='printf "index=%s host=%s\n" "$SLURM_ARRAY_TASK_ID" "$(hostname)"'
```

Expect four separate output files, with indices 0, 1, 2 and 3. At most two array elements run together. The hostname is assigned by Slurm and is not a fixed answer. This is an index demonstration; it does not measure parallel speedup.

## Before the room

- [ ] Open the learner homepage, fundamentals lesson, EESSI lesson, instructor guide and PDF while on the teaching network.
- [ ] Sign in with your own instructor account and second factor. Open the roster privately and one ordinary learner shell for projection.
- [ ] Confirm that the course portal, homes, scheduler and CPU nodes respond. Inspect free storage and `sinfo`; do not quote the diagram as the live inventory.
- [ ] Rehearse the exact Python and two-thread OpenMP commands above. Record both job IDs and outputs in a private directory. Check the maintained course rehearsal from the controller operator runbook as well.
- [ ] Confirm both Python module versions and `GCC/14.2.0` are available. Do not substitute a different version in a teaching script without a rehearsal.
- [ ] Hand each learner only their own welcome/setup information. Consumed setup links are not login links; an existing saved password stays usable after its setup URL expires.
- [ ] Keep an offline copy of the workbook and matching PDFs. Use the printed output for explanation if access fails, and call it example output rather than a live cluster result.

## Optional survey after the core checkpoints

Use this branch only when pairs have the Python result, the correct pi lines and a resource explanation by 03:20. It replaces the 03:20-03:50 array/storage block; it does not extend the class. Stop at 03:50 for the exit check. Choose individual previews when the group needs more practice with the core.

- Five minutes: [File systems](/filesystems/) and the lifetime decision for one result.
- Five minutes: [Moving data](/data-movement/pack-and-checksum.html), packing and checking a copy.
- Five minutes: [Many tasks](/many-tasks/), comparing the array with one pilot allocation.
- Five minutes: [Hybrid jobs](/hybrid-jobs/), drawing MPI ranks and OpenMP threads without starting a full hybrid exercise.
- Five minutes: [Performance](/performance/), calculating speedup 5 and efficiency 0.625 from 8.0 seconds on one core and 1.6 seconds on eight cores. These are example data, not a benchmark of the room's nodes.

The five previews take 25 minutes and leave five minutes of transition margin. No preview requires a database, a new software installation, profiler setup or a full transfer experiment. The links retain the detailed exercises for independent use.

## Parts II and III

Part II covers file systems, moving data and many tasks through QCG-PilotJob. Part III covers hybrid MPI/OpenMP and performance. Use the individual lesson instructor notes for their complete episodes. Cut `several-streams`, `other-tools` and `energy` before sacrificing the core exercise for those sessions.

The hybrid lesson is CC-BY 4.0, adapted from Introduccion a la Supercomputacion by Jose Luis Bosque, Borja Perez, Ramon Beivide and Carmen Martinez, Universidad de Cantabria, by the EuroCC NL team at SURF. Credits are on the lesson index.
