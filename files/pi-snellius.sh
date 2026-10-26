#!/bin/bash
#SBATCH --job-name=pi-one
#SBATCH --partition=rome
#SBATCH --cpus-per-task=16
#SBATCH --time=00:15:00
#SBATCH --output=pi-%j.out

# Snellius rome rounds a request up to 16 cores. Ask for that slice.
module purge
module load 2025
export SAMPLE_COUNT=1000
python3 pi_one.py
