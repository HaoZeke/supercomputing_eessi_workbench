There is no project budget and `accinfo` is not installed. `sacct` still reports core-seconds in `CPUTimeRAW`.

```bash
sacct -j JOBID --format=JobID,Elapsed,AllocCPUS,CPUTimeRAW
```
