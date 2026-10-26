# Site library

Three sites, shown together in grouped tabs:

| Directory | Tab |
| --- | --- |
| `SURF_Snellius_slurm` | Snellius |
| `SURF_Course_slurm` | Course cluster |
| `HPCC_MagicCastle_slurm` | Magic Castle |

Each directory has `_config_options.yml` and `snippets/`. An episode calls
one snippet:

```markdown
::: sites partition-request
:::
```

`tooling/expand_sites.py` fills `{{remote.login}}` from that site's config
and writes a `group-tab` when the three copies differ. A missing snippet
falls back to the Magic Castle file, with the requesting site's values.

`SUPERSURF_SITES=snellius` renders one site and skips the tabs.

The course cluster is a SURF Research Cloud workspace. CPU jobs use
`--partition=rome`. The login address is the one in the welcome note.
Whether mpiFileUtils is installed is still a `TODO(Rohit)` note on that
tab. The hybrid-jobs lesson carries a TODO for the Universidad de
Cantabria license.
