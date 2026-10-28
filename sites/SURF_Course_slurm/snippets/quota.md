`myquota` reports the filesystem containing your home. On BeeGFS its capacity display is shared space, not a personal quota.

```bash
myquota
df -h "$HOME" "/scratch/$USER"
du -sh "$HOME"
```
