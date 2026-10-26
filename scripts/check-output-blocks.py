# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Each printed output block must match the command it follows."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file


def run_local(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-euo", "pipefail"],
        input=script,
        text=True,
        capture_output=True,
        cwd=repo_file.ROOT,
        check=False,
    )


def run_eessi(script: str) -> subprocess.CompletedProcess[str]:
    sif = os.environ.get("EESSI_SIF", "/tmp/eessi-client.sif")
    work = os.environ.get("EESSI_WORKDIR", "/tmp/eessi-cache")
    for name in ("var-lib-cvmfs", "var-run-cvmfs", "home"):
        Path(work, name).mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["APPTAINER_BIND"] = (
        f"{work}/var-run-cvmfs:/var/run/cvmfs,{work}/var-lib-cvmfs:/var/lib/cvmfs"
    )
    env["APPTAINER_HOME"] = f"{work}/home:/home/ubuntu"
    if not Path(sif).exists():
        raise SystemExit(f"EESSI image not found at {sif}")
    return subprocess.run(
        [
            "apptainer",
            "exec",
            "--fusemount",
            "container:cvmfs2 software.eessi.io /cvmfs/software.eessi.io",
            sif,
            "bash",
            "-euo",
            "pipefail",
        ],
        input=script,
        text=True,
        capture_output=True,
        cwd=repo_file.ROOT,
        env=env,
        check=False,
    )


def main() -> None:
    org_files = list((repo_file.ROOT / "org_src").rglob("*.org"))
    checked = 0
    for path in org_files:
        blocks = repo_file.parse_output_blocks(path.read_text(encoding="utf-8"))
        for runner, script, expected in blocks:
            if runner == "eessi":
                result = run_eessi(script)
            elif runner == "local":
                result = run_local(script)
            else:
                raise SystemExit(f"unknown runner {runner} in {path}")
            # Apptainer prints CernVM-FS mount lines on stdout before the script.
            kept = [
                line
                for line in result.stdout.splitlines()
                if not line.startswith("CernVM-FS:")
            ]
            got = "\n".join(kept).strip("\n")
            if result.returncode != 0 or got != expected:
                print(f"output mismatch in {path.relative_to(repo_file.ROOT)} runner={runner}")
                print("exit", result.returncode)
                print("expected:")
                print(expected)
                print("got:")
                print(got)
                print("stderr:")
                print(result.stderr[-2000:])
                sys.exit(1)
            checked += 1
    if checked == 0:
        raise SystemExit("no output blocks found")
    print(f"output blocks ok ({checked})")


if __name__ == "__main__":
    main()
