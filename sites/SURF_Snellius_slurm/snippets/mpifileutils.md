EESSI does not ship mpiFileUtils. Load the site module your project uses, or build it with EasyBuild. Then, from a scratch directory:

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
SRC=/scratch-shared/$USER/run
DST=/scratch-shared/$USER/run-copy
srun dwalk -v "$SRC"
srun dcp -p "$SRC" "$DST"
```

`dwalk` counts files. `dcp -p` keeps permissions, group, and timestamps. `dsync` makes the destination match. `drm --dryrun` lists a delete. `dtar -c` writes a pax archive.
