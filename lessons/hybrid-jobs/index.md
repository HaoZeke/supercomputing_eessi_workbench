---
site: sandpaper::sandpaper_site
---

::: callout
## TODO(Rohit)

The license for this lesson is still open. The course README says the module was adapted from Introducción a la Supercomputación by José Luis Bosque, Borja Pérez, Ramón Beivide, and Carmen Martínez of the Universidad de Cantabria, by the EuroCC NL team at SURF. Keep that attribution. Do not treat it as permission to republish the text under CC-BY until the license is confirmed.
:::

This lesson runs three kernels under Slurm. AXPY and the dot product have a hybrid MPI and OpenMP program. Matrix multiplication is sequential, and you parallelise the outer loop yourself.

The EuroCC2 project page is <https://www.eurohpc-ju.europa.eu/research-innovation/our-projects/eurocc-2_en>.

::: prereq

- [ ] You can log in to Snellius or the course cluster and submit a Slurm job.
- [ ] You can load `module load 2025` and `module load foss/2025a`.

:::
