Pass the smaller request on the `sbatch` command line. Those options override the `#SBATCH` lines. Do not edit the script. Check the core count with `sinfo` first.

`Hyb-T-C` means T MPI tasks and C OpenMP threads.

Submit from each exercise directory:

| Exercise | Submission on two-core nodes |
| --- | --- |
| 1, sequential AXPY | `sbatch --cpus-per-task=1 submit-axpy.sh 10000000` |
| 2, AXPY MPI | `sbatch --ntasks=2 submit-axpy-hybrid.sh 10000000` |
| 3, sequential dot product | `sbatch --cpus-per-task=1 submit-dot.sh 10000000` |
| 4, dot product MPI | `sbatch --nodes=3 --ntasks=6 submit-dot-hybrid.sh 30000000` |
| 5, sequential matrix multiplication | `sbatch --cpus-per-task=1 submit-matmul.sh 500` |

The hostname exercise uses `--nodes=3 --ntasks=6 --ntasks-per-node=2`.

Columns that ask for 16 cores or more do not fit these nodes. Use `Hyb-2-1`, `Hyb-1-2`, `Hyb-3-2`, and `Hyb-6-1`. The last of those is `sbatch --nodes=3 --ntasks=6 --cpus-per-task=1 submit-axpy-hybrid.sh <N>`. Leave out the two largest vector sizes. They need more memory than these nodes have.
