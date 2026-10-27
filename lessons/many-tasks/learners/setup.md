---
title: Setup
---

Use the hands-on tree in this lesson:

`episodes/files/hands-on/`

Run each example from its own directory. The alternative scripts call `../../example_04` and `../../example_05`, so keep that layout.

You need Slurm and the Python the job scripts load. The scripts name their own modules. The episode tabs are the load lines for the machine in your welcome note.

Examples 2 and 4 need `input.tar.gz` in that example's directory. Both archives are in the tree.

On a two-core node the hands-on README uses:

```bash
sbatch --array=0-99%10 array_job.sh
QCG_MAX_INPUTS=100 sbatch --ntasks=2 qcg_job.sh
TIMES_FILE=times_short.txt sbatch --ntasks=2 pipeline.sh
TIMES_FILE=times_short.txt sbatch --ntasks=2 qcg_job.sh
```

The profile plot in example 5 uses the modules named in that example's README:

```bash
module load 2025
module load SciPy-bundle/2025.06-gfbf-2025a
module load matplotlib/3.10.3-gfbf-2025a
```

The last episode is optional. HyperQueue, Snakemake, and FireWorks each have a directory under `alternatives/`.
