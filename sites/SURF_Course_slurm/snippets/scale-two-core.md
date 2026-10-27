On a two-core node, pass the smaller request on the command line. Do not edit the script.

```bash
sbatch --cpus-per-task=2 pi.sh
sbatch --array=0-99%10 array_job.sh
QCG_MAX_INPUTS=100 sbatch --ntasks=2 qcg_job.sh
iend=8 wdir=TMPDIR sbatch run.sh
```

Check the core count with `sinfo` first.
