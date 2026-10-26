```bash
#SBATCH --partition=rome
rsync -a --partial /project/$USER/src/ "$TMPDIR/src/"
rsync -a --partial "$TMPDIR/src/" /project/$USER/out/
```

The course cluster is a SURF Research Cloud workspace. CPU jobs request the `rome` partition. Do not add `--constraint=scratch-node`.
