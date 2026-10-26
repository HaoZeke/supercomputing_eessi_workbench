---
title: "What limits a run"
teaching: 20
exercises: 10
---

::: questions

- How do you tell an I/O limit, a communication limit, a compute limit, and a memory limit apart?
- Which change matches which limit?

:::

::: objectives

- Separate I/O, communication, computation, and memory footprint using the distinctions in the deck.
- Match one symptom to each limit.

:::

An application has more than one level, and each level can dominate the time. The deck asks you to look at four of them on their own: I/O, communications, computations, and memory footprint.

## I/O

A parallel file system and a sequential file system do not move bytes the same way. You can measure read and write speed. The data can be ASCII or binary. Some file formats are sequential and some are parallel. The simplest evaluation is the elapsed time of the I/O itself.

The deck's table is a 10 million element vector of 64-bit floating-point values on an NVMe file system. Speeds are MB/s.

| Format | Operation | MB/s |
| --- | --- | --- |
| ASCII | Read | 29.7 |
| ASCII | Write | 24.9 |
| Binary | Read | 2666.4 |
| Binary | Write | 1586.5 |

`2666.4 / 29.7` is nearly 90, so the binary read in that table moves the same vector much faster. If the elapsed time of the run is the elapsed time of that read, the limit is I/O, and the format is part of the cause.

## Communication

Communication gets more expensive as the number of active processes grows, so speedup falls away from the ideal line. The cost depends on message size, on the topology of the network, and on synchronization. Changing it can require knowing that network. Some MPI libraries let you tune the algorithm at run time.

A communication-limited run is one where adding processes moves you further from ideal speedup, and the extra time tracks messages and waits.

## Computation

Ideal speedup, at fixed total work, is P when you use P processors. Dozens of tools measure sequential and parallel codes. Threaded codes, distributed codes, and GPU codes need different tools. Many of those tools read hardware counters. On Snellius the counters have to be turned on for the job. The roofline episode has the lines. The course cluster uses a different counter tool. The roofline tab holds that split.

A compute-limited run is one that approaches that ideal speedup, with the cores doing the arithmetic.

## Memory

The memory footprint is how much RAM the application holds. A large footprint can cause cache misses, and those misses show up as time. The footprint can also decide how large a node you must ask for. The deck's commands are:

```bash
valgrind --tool=massif PROG
ms_print massif.out.XXX
```

A memory-limited run is one that needs a bigger node because of RAM, or one whose time is cache misses.

## Changes, after you know the limit

The deck's list of changes is the third step of the life cycle. Pick from the limit you found.

- A faster model or method, or a faster library for the same method.
- Lower precision, from 64-bit floating point to 32-bit.
- A different data layout, from an array of structures to a structure of arrays.
- Less I/O, or a format that matches the measurement above.
- Less data movement, in cache or on the network.
- Code that knows the hardware, or different hardware.
- A smaller memory footprint.
- A different programming language.

:::: challenge
## Which limit is it?

Each note is one run. Name the limit: I/O, communication, compute, or memory.

1. A 10 million element vector of 64-bit values is read as ASCII at 29.7 MB/s and as binary at 2666.4 MB/s. The elapsed time of the run is the elapsed time of the read.
2. From 1 node to 32 nodes, speedup falls away from the ideal line. The extra time tracks message size, topology, and synchronization.
3. The total work stays fixed. On P processors the speedup is close to P, and the cores are doing the arithmetic.
4. The job only runs after you move it to a node with more RAM. `valgrind --tool=massif` shows a large footprint, and the time is cache misses.

::: solution
## Solution

1. I/O. The deck separates this limit by the elapsed time of the read or write, and by format. ASCII and binary on the same vector differ by the speeds in the table. A parallel format is the other lever the deck names.
2. Communication. The deck says this cost grows as more processes take part, and that it depends on message size, topology, and synchronization. The ideal-versus-real speedup curve is the picture of that gap.
3. Compute. The deck's ideal, at fixed total work, is a speedup of P on P processors. Counter tools are how you confirm the cores are doing that arithmetic. They are not themselves the limit.
4. Memory. The footprint is how much RAM the run holds. The deck says it can cause cache misses and can force you onto a larger node. `massif` is the measurement named for that footprint.
:::
::::

::: keypoints

- Look at I/O, communication, computation, and memory footprint separately.
- I/O: time the read and the write. On the deck's NVMe table, binary read is 2666.4 MB/s and ASCII read is 29.7 MB/s.
- Communication: speedup falls away from ideal as processes are added. Cost depends on message size, topology, and synchronization.
- Compute: at fixed total work the ideal speedup is P on P processors.
- Memory: the footprint can cause cache misses and can force a larger node. `valgrind --tool=massif` measures it.

:::
