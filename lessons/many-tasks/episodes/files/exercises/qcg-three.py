"""Three echo tasks under a local QCG-PilotJob manager."""

import os
import tempfile

from qcg.pilotjob.api.job import Jobs
from qcg.pilotjob.api.manager import LocalManager


def main() -> None:
    os.chdir(tempfile.mkdtemp())
    manager = LocalManager()
    jobs = Jobs()
    for i in range(3):
        jobs.add(
            name=f"job_{i}",
            exec="/usr/bin/printf",
            args=[f"task-{i}\\n"],
            stdout=f"out_{i}.txt",
            numCores={"exact": 1},
        )
    manager.submit(jobs)
    manager.wait4all()
    manager.finish()
    print("qcg-finished")
    print(open("out_0.txt", encoding="utf-8").read().strip())


if __name__ == "__main__":
    main()
