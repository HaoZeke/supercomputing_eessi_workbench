```bash
#SBATCH --partition=rome
#SBATCH --constraint=scratch-node
rsync -a --partial /scratch-shared/$USER/src/ "$TMPDIR/src/"
rsync -a --partial "$TMPDIR/src/" /scratch-shared/$USER/out/
```

The copy back has to be inside the script. The node disk is removed when the job ends.
