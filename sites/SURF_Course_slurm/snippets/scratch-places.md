| Place | Path | What it is for |
| --- | --- | --- |
| Home | `/home/$USER` | Shared with the compute nodes |
| Project | `/project` | Shared |
| Scratch | `/scratch` | Shared BeeGFS scratch on the course cluster |
| Node disk | `$TMPDIR` | This job only. Removed when the job ends |

There is no `/scratch-shared`, no `/scratch-node`, and no `/archive`.
