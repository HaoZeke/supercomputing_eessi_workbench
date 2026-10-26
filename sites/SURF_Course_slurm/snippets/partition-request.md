::: callout
## TODO(Rohit)

The course cluster name and partition for the next run are still open.
The workbench uses a Magic Castle workspace and `--partition=thin_course`.
The course README says SURF Research Cloud workspaces and the partition `rome`.
The fundamentals deck says those two partition names point at the same nodes.
This tab does not choose.
:::

```bash
#SBATCH --partition=PARTITION
```

`PARTITION` is a placeholder. Shrink `--ntasks` and `--cpus-per-task` on the `sbatch` line for the small nodes. The scripts stay as published.
