---
title: "The roofline"
teaching: 25
exercises: 20
---

::: questions

- What is arithmetic intensity, and what is the ridge?
- How does the deck turn throughput 6.7257 and bandwidth 2.6767 into 2.5 FLOP/byte?

:::

::: objectives

- Place a kernel on the memory side or the compute side of the ridge.
- Count FLOPs for an add, a multiply, and a dense matrix product.
- Read the deck's uProf example as 2.5 FLOP/byte, and use the counter tab for your machine.

:::

## Two roofs

A roofline plots how fast a kernel runs against how much arithmetic it does per byte it moves. The vertical axis is performance, in GFLOPS. The horizontal axis is arithmetic intensity, in FLOP/byte.

The sloping roof is memory bandwidth. The flat roof is peak performance. They meet at the ridge point. Left of the ridge the kernel is memory-bound: it waits on bytes. Right of the ridge it is compute-bound: it waits on the arithmetic peak. The picture shows which optimisation to do first. A memory-bound kernel speeds up when it moves fewer bytes, or when the machine moves bytes faster. A higher arithmetic peak sits on the other side of the ridge.

Double precision and single precision can be two flat roofs. The higher one is the single-precision peak. The lower one is the double-precision peak.

![Two bounds for a program. The nodes drawn are bandwidth roof, peak roof, and your code.](fig/roofline.svg){alt='Two bounds for a program. The nodes drawn are bandwidth roof, peak roof, and your code.'}

The figure's bandwidth roof is the sloping side. The peak roof is the flat side. Your kernel is a point underneath one of them. The ridge is the corner where the two roofs meet. The figure has no numeric intensity for that corner. Compare a measured intensity with the ridge of the machine you measured.

## Counting FLOPs

An addition is 1 FLOP. A multiplication is 1 FLOP. One add and one multiply on each of N elements is `2N` FLOP.

If you know the algorithm, you can use its complexity. A generic dense matrix-matrix product is about `O(N^3)` FLOP. The matching total for the usual inner step, one multiply and one add, is about `2 N^3` FLOP. An FFT is about `O(N log2(N))` FLOP. The big-O form often leaves out the total count. `O(N^3)` says how the count grows. `2 N^3` is a count.

A large code base is a poor place to do this by hand. The deck's answer is to use a performance tool. The reference page lists the tools from the deck. For a roofline, the ones that read counters are PAPI, likwid, and uProf. Score-P and Scalasca are the MPI and OpenMP analysis path named alongside them.

## The deck's uProf example

On Snellius the deck loads uProf and asks it for a roofline. The course cluster does not use this command. The tab below is the split: uProf on Snellius, `perf` and PAPI on the course cluster.

```bash
module purge
module load 2025
module load AMD-uProf/5.1.701
AMDuProfPcm roofline -X -o res.csv -- PROG ARGS
```

The sample profile data in the deck is:

```text
Throughput,6.7257
Bandwidth,2.6767
```

uProf reports throughput in GFLOP/s and bandwidth in GB/s. Divide them:

```text
AI = 6.7257 / 2.6767 = 2.5 FLOP/byte
```

That 2.5 is the arithmetic intensity of this sample. Compare it with the roofline ridge on the machine that produced the file. Use this 2.5. The deck gives no separate ridge number to subtract from it. Left of the ridge is memory-bound. Right of the ridge is compute-bound.

::: sites perf-counters
:::

:::: challenge
## 2.5 FLOP/byte, and which side of the ridge

Using the deck's sample, write `6.7257 / 2.6767` as a single intensity with units.

An update `y[i] = a * x[i] + y[i]` does one multiply and one add on each element. How many FLOP is that for N elements?

A measured point sits left of the ridge. Which roof is it under, and which kind of change comes first: moving fewer bytes, or raising the arithmetic peak?

::: solution
## Solution

`6.7257 / 2.6767 = 2.5` FLOP/byte. Throughput was GFLOP/s and bandwidth was GB/s, so the ratio is FLOP/byte. Do not replace 2.5 with another intensity.

N elements, one multiply and one add each, is `2N` FLOP.

Left of the ridge is the bandwidth roof. The kernel is memory-bound. Moving fewer bytes, or raising the bytes the machine can move, is the change that can lift the point. Raising the arithmetic peak moves a roof the kernel is not on.
:::
::::

::: keypoints

- Arithmetic intensity is FLOP/byte. The ridge is where the bandwidth roof meets the peak roof.
- Left of the ridge is memory-bound. Right of the ridge is compute-bound.
- An add is 1 FLOP and a multiply is 1 FLOP, so N of each is `2N` FLOP. Dense matrix multiplication is about `2 N^3` FLOP, which `O(N^3)` does not state.
- The deck's uProf sample is `AMDuProfPcm roofline -X -o res.csv`, and `6.7257 / 2.6767 = 2.5` FLOP/byte.
- The course tab is `perf` and PAPI, not uProf.

:::
