---
title: "Idle time"
teaching: 10
exercises: 20
---

::: questions

- What does the bash pipeline wait for at the end of each block?
- What does QCG-PilotJob do when a task ends and a core is free?

:::

::: objectives

- Compare `pipeline.sh` and `qcg_job.sh` on `times_short.txt`.
- Read the block size off `SLURM_NTASKS`, and the `wait` at the end of each block.
- Plot both outputs with `plot_profile.py`.

:::

## Two ways through the same sleeps

Example 5 runs the same list of sleeps two ways. `sleep.py` sleeps for the number of seconds you pass and prints one line: `TASK`, the CPU id, the start time, and the end time.

The README's example of that line, from `python sleep.py 7`, is:

```text
TASK,54,1763290002.014343,1763290009.014470
```

The CPU number and the timestamps are from that example. The two times differ by about 7 seconds, which is the argument.

`pipeline.sh` is a Slurm job of 1 node and 16 tasks, one hour, partition `rome`, output `pipeline.%j.out`. `qcg_job.sh` is 1 node and 16 tasks, 40 minutes, partition `rome`, output `qcg.%j.out`. Both default to `times.txt`. `TIMES_FILE` selects another file.

`times.txt` has 160 lines. `times_short.txt` is the first 32 of those lines, unchanged. They sum to 338 seconds. The longest of the 32 is 56 and the shortest is 2.

On 2 cores the hands-on README runs both with that short file, so both use the same number of slots:

```bash
TIMES_FILE=times_short.txt sbatch --ntasks=2 pipeline.sh
TIMES_FILE=times_short.txt sbatch --ntasks=2 qcg_job.sh
```

The comment in `pipeline.sh` says the block size is the number of tasks Slurm gave the job, 16 on the `#SBATCH` line, so the comparison with QCG stays fair. `--ntasks=2` changes that number for both commands. Leave the `#SBATCH --ntasks=16` lines in the files.

The README's warning on the lengths: `times_short.txt` keeps the original task lengths. Shorter tasks would make QCG's start-up time per task count for more than the idle time it saves, and the comparison would turn around.

## The pipeline waits for the slowest task in the block

`pipeline.sh` reads the times, then sends the sleeps in blocks. This is the loop:

```bash
times=${TIMES_FILE:-times.txt}
block=${SLURM_NTASKS:-16}
mapfile -t nums < "$times"

for ((i=0; i<${#nums[@]}; i+=block)); do
    for num in "${nums[@]:i:block}"; do
        python sleep.py "$num" &
    done
    wait
done
```

`wait` returns when every background sleep in that block has finished. With `--ntasks=2` the lines stay in order, so 56 shares a block with the 4 that precedes it in `times_short.txt`. The 4-second sleep finishes, and `wait` holds the next block until the 56-second sleep ends.

QCG fills slots as tasks end. `qcg_job.py` adds every line of `TIMES_FILE` as its own job (`exec='python3'`, arguments `sleep.py` and the seconds, `iteration=1`) and then calls `manager.wait4all()`. The tasks share the allocation. When one finishes, the manager can start another on that core. There is no `wait` between blocks, because there are no blocks.

`qcg_job.sh` records the wall clock around that Python, then concatenates the task files:

```bash
START=$( date +%s )
python qcg_job.py
END=$( date +%s )

echo START,$START
cat $TMPDIR/qcg_*.out
echo END,$END
```

`pipeline.sh` prints `START` before the loop and `END` after it. The `TASK` lines from `sleep.py` fall between them in the Slurm output.

## The plot

`plot_profile.py` reads `START`, `END`, and every `TASK` line. The lanes are the CPU number each task reported at the start. From `example_05`, after both jobs finish:

```bash
module load 2025
module load SciPy-bundle/2025.06-gfbf-2025a
module load matplotlib/3.10.3-gfbf-2025a

python plot_profile.py pipeline.<SLURM_JOB_ID>.out
python plot_profile.py qcg.<SLURM_JOB_ID>.out
```

The output names follow the scripts: `pipeline.%j.out` and `qcg.%j.out`. The README says you can open the PNG files in the Open OnDemand file browser, or copy them to your own computer.

The measured spans and idle percentages for this pair are in the next episode. They come from one run. This episode is the two scripts.

:::: challenge

## Who waits for 56?

`times_short.txt` contains 56. On `--ntasks=2`, that value shares a block with the 4 written just before it. Which script waits for 56 before it starts the next pair, and which line does the waiting?

::: solution

## Solution

`pipeline.sh`. The inner loop starts one `sleep.py` per value in the block, in the background. The bare `wait` after that loop returns only when every sleep in the block has finished. In the block that holds 4 and 56, that means waiting for 56.

`qcg_job.py` submits the whole file and calls `manager.wait4all()` once. A finished task frees a core, and the manager can start the next sleep on it. The 2-second task does not hold the allocation until 56 finishes.

:::

::::

:::: challenge

## Same slots

You have a 2-core node. Write the two `sbatch` lines that compare the pipeline and QCG on the short file. What must you leave unchanged in the sleep times, and why?

::: solution

## Solution

```bash
TIMES_FILE=times_short.txt sbatch --ntasks=2 pipeline.sh
TIMES_FILE=times_short.txt sbatch --ntasks=2 qcg_job.sh
```

`times_short.txt` stays as the first 32 lines of `times.txt`. The hands-on README says shorter tasks would make QCG's start-up time per task count for more than the idle time it saves, and the comparison would turn around. `--ntasks=2` sets the pipeline's block size and QCG's slot count to the same number, because the block size is `SLURM_NTASKS`.

:::

::::

::: keypoints

- `pipeline.sh` runs sleeps in blocks of `SLURM_NTASKS` and `wait`s for the whole block.
- The slowest task in a block holds the next block. A finished short task in that block does not start new work.
- QCG submits every line and fills a free core when a task ends.
- `times_short.txt` is the first 32 of 160 lines, original lengths, summing to 338 seconds.
- On 2 cores, both scripts take `TIMES_FILE=times_short.txt` and `--ntasks=2`.

:::
