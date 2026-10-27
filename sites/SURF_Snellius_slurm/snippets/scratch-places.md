| Place | Path | Kept for | Quota |
| --- | --- | --- | --- |
| Home | `/home/$USER` | Backed up, three weeks of deleted files | 200 GiB |
| Scratch-shared | `/scratch-shared/$USER` | About 14 days | Counted in the 8 TiB scratch quota |
| Scratch-local | `$TMPDIR` | This job | Counted in the scratch quota |
| Scratch-node | `$TMPDIR` with `--constraint=scratch-node` | Until the job ends, then removed | No quota |
| Project | `/projects` | The life of the project | Project quota |
| Archive | `/archive/$USER` | Long term, tape | Login and staging nodes only |
