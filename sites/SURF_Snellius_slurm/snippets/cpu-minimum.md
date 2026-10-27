On `rome` the smallest allocation is 1/8 of a node. A node has 128 cores, so the minimum is 16 cores.

```bash
#SBATCH --partition=rome
#SBATCH --cpus-per-task=16
```
