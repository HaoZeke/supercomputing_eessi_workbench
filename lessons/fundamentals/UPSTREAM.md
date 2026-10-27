# Upstream

This lesson vendors [carpentries-incubator/hpc-intro](https://github.com/carpentries-incubator/hpc-intro).

| | |
| --- | --- |
| Commit | `7081080674aceeb0a4bc57b9348da22d876af802` |
| Date | 2026-10-05 |
| Subject | Merge pull request #523 from carpentries-incubator/update/workbench-docker-version |
| License | CC-BY 4.0, Copyright (c) The Carpentries |
| Maintainer | Christina Koch |
| Authors | `AUTHORS` |

The file `UPSTREAM` holds that commit id on one line.

What this copy changes:

- `config.yaml`: title "Fundamentals of HPC", carpentry `supersurf`, contact `rgoswami@ieee.org`, source this repository, URL `https://supersurf.rgoswami.me/fundamentals/`, life cycle `pre-alpha`. The Carpentries analytics key is not set.
- `episodes/files/customization/HPCC_MagicCastle_slurm/_config_options.yml`: `url` and `baseurl`, so the upstream discuss page can build.
- README attribution at the top.

`LICENSE.md` and `AUTHORS` are the upstream files. The Magic Castle snippets are the upstream files. SURF replacements for the snippets that name a Magic Castle partition or a pilot EESSI path are under `episodes/files/customization/SURF_Snellius_slurm/` and `SURF_Course_slurm/`.

Two episodes are not from hpc-intro: `surf-accounting.md` and `python-and-openmp.md`. Their scripts and numbers come from `fix/slides-fundamentals-source` at `2ebb95294418d5831143e393e93b294af39464b1`. See `episodes/files/hands-on/PROVENANCE.md`.
