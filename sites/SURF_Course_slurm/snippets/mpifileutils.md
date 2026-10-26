mpiFileUtils is installed on this SURF Research Cloud workspace. It is not an EESSI module. EESSI 2023.06 and 2025.06 do not provide it.

```bash
sbatch dcp.slurm
```

```bash
#!/bin/bash
#SBATCH --job-name=dcp
#SBATCH --partition=rome
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --time=01:00:00
#SBATCH --output=dcp-%j.out
set -eu
SRC=/scratch/$USER/run
DST=/scratch/$USER/run-copy
srun dwalk -v "$SRC"
srun dcp -p "$SRC" "$DST"
```

`dwalk` counts files. `dcp -p` keeps permissions, group, and timestamps. `dsync` makes the destination match. `drm --dryrun` lists a delete. `dtar -c` writes a pax archive.
