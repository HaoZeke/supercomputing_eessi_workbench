# Instructors

Three sessions, four hours each. The full lesson is what you build. The schedule is what you teach. Episodes marked "cut first" go before anything else when the room is short: `several-streams` (moving data), `other-tools` (many tasks), `energy` (performance).

## Before the room

- [ ] Logins work for Snellius or the course cluster, and the welcome note has the address.
- [ ] `module load 2025` then `module load Python/3.13.5-GCCcore-14.3.0` then `python3 --version` prints `Python 3.13.5`.
- [ ] On the course cluster, `module load 2024` still selects EESSI 2025.06, and QCG-PilotJob loads from the site build. It is not an EESSI module.
- [ ] You can show the three site tabs. The course cluster is a SURF Research Cloud workspace, and its tab requests `--partition=rome`. The published scripts keep the `#SBATCH` lines they were written with. Overrides go on the `sbatch` command.
- [ ] The hybrid lesson is CC-BY 4.0. It is adapted from Introducción a la Supercomputación by José Luis Bosque, Borja Pérez, Ramón Beivide, and Carmen Martínez, Universidad de Cantabria, by the EuroCC NL team at SURF. The credits are on the lesson index.

## How a session runs

Each lesson is a Carpentries Workbench site under its own path. Learners open <https://supersurf.rgoswami.me/> and follow the lesson link. Setup for all three machines is the [setup page](setup.html).

Part I is the EESSI lesson and fundamentals (hpc-intro plus the Snellius accounting episode and the OpenMP pi exercise). Part II is file systems, moving data, and many tasks through QCG-PilotJob. Part III is hybrid MPI/OpenMP and performance. If Part II overruns, cut `several-streams` and `other-tools` and keep the array and the QCG dependency exercise.

Show one tab for the machine in the room and leave the other two visible, so a Snellius command and a course-cluster command are not mixed into one script.
