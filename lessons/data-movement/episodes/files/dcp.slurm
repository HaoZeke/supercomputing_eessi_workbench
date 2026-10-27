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
