```bash
rsync -a --partial "$HOME/src/" "$TMPDIR/src/"
rsync -a --partial "$TMPDIR/src/" "$HOME/out/"
```
