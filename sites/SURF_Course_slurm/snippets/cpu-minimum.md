::: callout
## TODO(Rohit)

The course cluster name and partition for the next run are still open.
The workbench uses a Magic Castle workspace and `--partition=thin_course`.
The course README says SURF Research Cloud workspaces and the partition `rome`.
The fundamentals deck says those two partition names point at the same nodes.
This tab does not choose.
:::

The nodes in the course are small. A two-core override is the usual request when `sinfo` shows two cores:

```bash
#SBATCH --cpus-per-task=2
```

Check `sinfo` before you copy that number.
