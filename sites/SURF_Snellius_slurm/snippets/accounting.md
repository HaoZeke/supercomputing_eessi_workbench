The `rome` row of the accounting table is 521 nodes, 128 cores, 256 GB, 128 SBU per hour, smallest allocation 1/8 of a node.

16 cores is 1/8 of 128, so it is the smallest `rome` job. At 128 SBU per node-hour that is 16 SBU per hour. Two hours is 32 SBU.

```text
cores x hours x (SBU per node-hour / cores per node)
16 x 2 x (128 / 128) = 32
```
