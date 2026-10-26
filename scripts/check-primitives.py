# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Unit tests for the shared helpers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file


class Helpers(unittest.TestCase):
    def test_org_to_md(self) -> None:
        self.assertEqual(
            repo_file.org_to_md(repo_file.ROOT / "org_src" / "index.org").name,
            "index.md",
        )
        episode = repo_file.org_to_md(repo_file.ROOT / "org_src" / "episodes" / "slurm-jobs.org")
        self.assertEqual(episode, repo_file.ROOT / "episodes" / "slurm-jobs.md")

    def test_efficiency(self) -> None:
        self.assertAlmostEqual(repo_file.efficiency(8.0, 8, 1.6), 0.625)

    def test_dot_labels_ignore_edges(self) -> None:
        text = '\n'.join(
            [
                '  laptop [label="laptop"];',
                '  login [label="login node"];',
                '  laptop -> login [label="ssh"];',
            ]
        )
        self.assertEqual(repo_file.dot_node_labels(text), ["laptop", "login node"])

    def test_output_blocks(self) -> None:
        text = """
#+begin_src bash
# runner: eessi
printf 'ok\\n'
#+end_src

#+begin_output
ok
#+end_output
"""
        blocks = repo_file.parse_output_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0][0], "eessi")
        self.assertIn("printf", blocks[0][1])
        self.assertNotIn("runner:", blocks[0][1])
        self.assertEqual(blocks[0][2], "ok")

    def test_front_matter(self) -> None:
        text = "---\ntitle: \"T\"\nteaching: 30\nexercises: 15\n---\n"
        self.assertEqual(repo_file.front_matter_minutes(text), (30, 15))

    def test_pipe_table(self) -> None:
        text = "| A | B |\n|---|---|\n| 1 | 2 |\n"
        self.assertEqual(repo_file.parse_pipe_table(text), [["A", "B"], ["1", "2"]])


if __name__ == "__main__":
    unittest.main(verbosity=1)
