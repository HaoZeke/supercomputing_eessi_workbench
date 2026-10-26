```bash
#SBATCH --ear=on
#SBATCH --ear-policy=monitoring
```

After the job:

```bash
eacct -j JOBID
```

Read POWER (W) and ENERGY (J).
