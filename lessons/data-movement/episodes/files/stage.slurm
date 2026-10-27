#!/bin/bash
#SBATCH --job-name=stage
#SBATCH --partition=rome
#SBATCH --constraint=scratch-node
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --output=stage-%j.out
set -eu
rsync -a --partial \
  /scratch-shared/$USER/src/ "$TMPDIR/src/"
rsync -a --partial \
  "$TMPDIR/src/" /scratch-shared/$USER/out/
