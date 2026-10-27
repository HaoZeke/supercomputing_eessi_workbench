```bash
#SBATCH --partition=rome
#SBATCH --constraint=scratch-node
```

Scratch-node is NVMe on the node. It is removed when the job ends. It is not on every node. Fat nodes have it, and a subset of `rome`, `genoa`, and GPU nodes have it.
