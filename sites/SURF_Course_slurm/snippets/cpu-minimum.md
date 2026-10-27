The nodes in this SURF Research Cloud workspace can be small. A two-core override is the usual request when `sinfo` shows two cores:

```bash
#SBATCH --cpus-per-task=2
```

Check `sinfo` before you copy that number. CPU jobs still request `--partition=rome`.
