# Supercomputing with EESSI

A one-day Carpentries Workbench lesson on a shared supercomputer: logging in, the EESSI software stack, Slurm, file systems, many small tasks, and a first look at timing.

The episode sources are Org files in `org_src/`. `pixi run build` exports them to Workbench Markdown. The slide decks for the SURF course live in [introduction-to-supercomputing](https://github.com/HaoZeke/introduction-to-supercomputing). How a module is built is [What EasyBuild is doing](https://hpceb.rgoswami.me/).

```sh
pixi run build
pixi run gate
pixi run slides
pixi run site
```

`pixi run check` runs the lesson checks, including the offline exercises and the EESSI output blocks.
