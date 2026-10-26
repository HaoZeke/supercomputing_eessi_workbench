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
rsync -a --partial /project/$USER/src/ "$TMPDIR/src/"
rsync -a --partial "$TMPDIR/src/" /project/$USER/out/
```

Do not add `--constraint=scratch-node`.
