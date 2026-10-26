---
site: sandpaper::sandpaper_site
---

This lesson runs three kernels under Slurm. AXPY and the dot product have a hybrid MPI and OpenMP program. Matrix multiplication is sequential, and you parallelise the outer loop yourself.

The EuroCC2 project page is <https://www.eurohpc-ju.europa.eu/research-innovation/our-projects/eurocc-2_en>.

## Credits

This lesson is adapted from *Introducción a la Supercomputación* by José Luis Bosque, Borja Pérez, Ramón Beivide, and Carmen Martínez, Universidad de Cantabria, by the EuroCC NL team at SURF. License: CC-BY 4.0. The names are also in `AUTHORS` and `CITATION.cff`.

::: prereq

- [ ] You can log in to Snellius or the course cluster and submit a Slurm job.
- [ ] You can load `module load 2025` and `module load foss/2025a`.

:::
