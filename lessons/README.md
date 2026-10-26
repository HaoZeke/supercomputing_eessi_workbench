# Lessons

Each directory is one Carpentries Workbench lesson. The site build renders
it and copies the HTML to `https://supersurf.rgoswami.me/<slug>/`.

| Slug | Lesson |
| --- | --- |
| `eessi` | The EESSI software stack |
| `fundamentals` | HPC fundamentals, vendored from hpc-intro with SURF customizations |
| `filesystems` | File systems |
| `data-movement` | Moving data |
| `many-tasks` | Arrays, QCG-PilotJob, and other workflow tools |
| `hybrid-jobs` | Hybrid MPI and OpenMP |
| `performance` | Performance analysis |

Shared site tabs live in `sites/`. `tooling/assemble-site.sh` builds the
combined site.
