#!/usr/bin/env python3
"""Fixture checks for the shared site tabs."""

import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import expand_sites as ex


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")


class ExpandTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.lesson = self.root / "lessons" / "demo"
        self.lesson.mkdir(parents=True)
        os.environ.pop("SUPERSURF_SITES", None)
        write(
            self.root / "sites" / "HPCC_MagicCastle_slurm" / "_config_options.yml",
            """
            remote:
              login: cluster.hpc-carpentry.org
              prompt: "[yourUsername@login1 ~]$"
            sched:
              queue:
                testing: cpubase_bycore_b1
            """,
        )
        write(
            self.root / "sites" / "SURF_Snellius_slurm" / "_config_options.yml",
            """
            remote:
              login: snellius.surf.nl
              prompt: "[YOUR_LOGIN@int4 ~]$"
            sched:
              queue:
                testing: rome
            """,
        )
        write(
            self.root / "sites" / "SURF_Course_slurm" / "_config_options.yml",
            """
            remote:
              login: MANAGER
              prompt: "[YOUR_LOGIN@LOGIN ~]$"
            sched:
              queue:
                testing: PARTITION
            """,
        )
        write(
            self.root / "sites" / "HPCC_MagicCastle_slurm" / "snippets" / "ssh-login.md",
            """
            ```bash
            ssh {{remote.user}}@{{remote.login}}
            ```
            """,
        )
        # remote.user is only on the base after we add it. Put it on the base.
        write(
            self.root / "sites" / "HPCC_MagicCastle_slurm" / "_config_options.yml",
            """
            remote:
              login: cluster.hpc-carpentry.org
              user: yourUsername
              prompt: "[yourUsername@login1 ~]$"
            sched:
              queue:
                testing: cpubase_bycore_b1
            """,
        )
        write(
            self.root / "sites" / "SURF_Snellius_slurm" / "snippets" / "ssh-login.md",
            """
            ```bash
            ssh YOUR_LOGIN@{{remote.login}}
            ```
            """,
        )
        write(
            self.root / "sites" / "HPCC_MagicCastle_slurm" / "snippets" / "partition-request.md",
            """
            ```bash
            #SBATCH --partition={{sched.queue.testing}}
            ```
            """,
        )
        write(
            self.root / "sites" / "SURF_Course_slurm" / "snippets" / "partition-request.md",
            """
            TODO(Rohit): the course cluster name and partition are still open.

            ```bash
            #SBATCH --partition={{sched.queue.testing}}
            ```
            """,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_tabs_when_snippets_differ(self):
        text = "::: sites ssh-login\n:::\n"
        out = ex.expand_text(text, self.lesson)
        self.assertIn("### Snellius", out)
        self.assertIn("ssh YOUR_LOGIN@snellius.surf.nl", out)
        self.assertIn("### Magic Castle", out)
        self.assertIn("group-tab", out)
        self.assertNotIn("{{", out)

    def test_fallback_uses_requesting_site_values(self):
        text = "::: sites ssh-login\n:::\n"
        out = ex.expand_text(text, self.lesson)
        # Course cluster has no ssh-login snippet, so the Magic Castle file is
        # filled with the course login.
        self.assertIn("ssh yourUsername@MANAGER", out)

    def test_identical_snippets_skip_tabs(self):
        same = "```bash\nhostname\n```\n"
        for site in ex.ORDER_NAMES:
            write(self.root / "sites" / site / "snippets" / "same.md", same)
        out = ex.expand_text("::: sites same\n:::\n", self.lesson)
        self.assertNotIn("group-tab", out)
        self.assertIn("hostname", out)

    def test_code_fence_with_config(self):
        text = "```bash\n`r config$remote$prompt` squeue\n```\n"
        out = ex.expand_text(text, self.lesson)
        self.assertIn("[YOUR_LOGIN@int4 ~]$ squeue", out)
        self.assertIn("[yourUsername@login1 ~]$ squeue", out)
        self.assertNotIn("config$", out)

    def test_single_site_env(self):
        os.environ["SUPERSURF_SITES"] = "snellius"
        try:
            out = ex.expand_text("::: sites ssh-login\n:::\n", self.lesson)
        finally:
            os.environ.pop("SUPERSURF_SITES", None)
        self.assertNotIn("group-tab", out)
        self.assertIn("snellius.surf.nl", out)
        self.assertNotIn("MANAGER", out)

    def test_rmd_snippet_call(self):
        write(
            self.lesson / "episodes" / "files" / "customization" / "HPCC_MagicCastle_slurm" / "snippets" / "scheduler" / "basic-job-script.Rmd",
            "Submitted batch job 7\n",
        )
        write(
            self.lesson / "episodes" / "files" / "customization" / "SURF_Snellius_slurm" / "snippets" / "scheduler" / "basic-job-script.Rmd",
            "Submitted batch job 4401218\n",
        )
        text = "```{r, echo=FALSE, results='asis'}\nsnippets('scheduler/basic-job-script.Rmd')\n```\n"
        out = ex.expand_text(text, self.lesson)
        self.assertIn("4401218", out)
        self.assertIn("### Snellius", out)
        self.assertNotIn("```{r", out)

    def test_course_todo_mentions_both_sources(self):
        out = ex.expand_text("::: sites partition-request\n:::\n", self.lesson)
        self.assertIn("TODO(Rohit)", out)
        self.assertIn("--partition=PARTITION", out)


if __name__ == "__main__":
    unittest.main()
