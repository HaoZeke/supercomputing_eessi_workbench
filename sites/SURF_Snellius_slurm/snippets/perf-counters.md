```bash
#SBATCH --constraint=hwperf
AMDuProfPcm roofline -X -o res.csv -- ./matmul 1000
```

`--constraint=hwperf` places the job on a node where the counters are readable. uProf reports throughput in GFLOP/s and bandwidth in GB/s.
