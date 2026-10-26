The course cluster is a SURF Research Cloud workspace. CPU jobs request the `rome` partition.

```bash
#SBATCH --partition=rome
```

Shrink `--ntasks` and `--cpus-per-task` on the `sbatch` line when `sinfo` shows small nodes. The scripts stay as published.
