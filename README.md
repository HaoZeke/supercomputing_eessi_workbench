# Supercomputing with EESSI

Seven Carpentries Workbench lessons in this repository, published as one site at <https://supersurf.rgoswami.me/>. A lesson lives in `lessons/<slug>/` and is served at `https://supersurf.rgoswami.me/<slug>/`.

The four-hour Introduction to HPC route is Part I. Its elapsed timetable includes a break, exercise checkpoints and a closing margin; the class plan gives the running order and learner slide download. The full episode estimates describe reference material beyond the selected route.

The landing page, the setup page, and the instructor page are rendered from `schedule.yaml` and `site_src/` by `tooling/schedule.py`. The published class uses one course-cluster path and starts with Open OnDemand. Alternative site configurations remain in `sites/`; select them explicitly with `SUPERSURF_SITES`.

```sh
pixi run site
pixi run check-site
```

That builds every lesson and writes the combined site to `site/docs/`, including the CNAME `supersurf.rgoswami.me`.

The course text is [sara-nl/introduction-to-supercomputing](https://github.com/sara-nl/introduction-to-supercomputing) and the fork [HaoZeke/introduction-to-supercomputing](https://github.com/HaoZeke/introduction-to-supercomputing). Fundamentals vendors [hpc-intro](https://github.com/carpentries-incubator/hpc-intro) at `7081080674aceeb0a4bc57b9348da22d876af802` (CC-BY 4.0, The Carpentries). How a module is built is [What EasyBuild is doing](https://hpceb.rgoswami.me/).

The one-day lesson that used to sit at the repository root has been replaced by this course. Old episode URLs redirect from the landing-page build.
