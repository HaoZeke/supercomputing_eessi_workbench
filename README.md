# Supercomputing with EESSI

Seven Carpentries Workbench lessons in this repository, published as one site at <https://supersurf.rgoswami.me/>. A lesson lives in `lessons/<slug>/` and is served at `https://supersurf.rgoswami.me/<slug>/`.

The landing page, the setup page, and the instructor page are rendered from `schedule.yaml` and `site_src/` by `tooling/schedule.py`. Shared site tabs (Snellius, the course cluster, Magic Castle) live in `sites/`.

```sh
bash tooling/assemble-site.sh
```

That builds every lesson and writes the combined site to `site/docs/`, including the CNAME `supersurf.rgoswami.me`.

The course text is [sara-nl/introduction-to-supercomputing](https://github.com/sara-nl/introduction-to-supercomputing) and the fork [HaoZeke/introduction-to-supercomputing](https://github.com/HaoZeke/introduction-to-supercomputing). Fundamentals vendors [hpc-intro](https://github.com/carpentries-incubator/hpc-intro) at `7081080674aceeb0a4bc57b9348da22d876af802` (CC-BY 4.0, The Carpentries). How a module is built is [What EasyBuild is doing](https://hpceb.rgoswami.me/).

The one-day lesson that used to sit at the repository root has been replaced by this course. Old episode URLs redirect from the landing-page build.
