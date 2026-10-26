#!/bin/bash
#SBATCH --job-name=pi-array
#SBATCH --partition=thin_course
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --array=0-3
#SBATCH --output=pi-%A_%a.out

module purge
module load 2025
sizes=(1000 2000 4000 8000)
export SAMPLE_COUNT="${sizes[$SLURM_ARRAY_TASK_ID]}"
python3 pi_one.py
