#!/bin/bash
#SBATCH --job-name=pi-one
#SBATCH --partition=thin_course
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --output=pi-%j.out

# The serial pi program needs one CPU in the classroom partition.
module purge
module load 2025
export SAMPLE_COUNT=1000
python3 pi_one.py
