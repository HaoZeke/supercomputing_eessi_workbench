# Setup

You need a terminal and one of the three machines below. You do not need all three. The lesson pages link back here.

## Snellius

Snellius is the Dutch national supercomputer. SURF sends the account mail after your project has a login. The public description of the machine is at <https://www.surf.nl/en/services/compute/snellius-the-national-supercomputer>.

```bash
ssh YOUR_LOGIN@snellius.surf.nl
```

Sign in at <https://portal.cua.surf.nl/> before the first SSH login. If the network you are on is not trusted, the welcome mail names a door node. Use that host instead of `snellius.surf.nl`.

A browser session through Open OnDemand (<https://ondemand.snellius.surf.nl/>) is still a login node. Do not start the long run there.

## The course cluster

TODO(Rohit): the course cluster name and partition for the next run are still open. The workbench uses a Magic Castle workspace and `--partition=thin_course`. The course README says SURF Research Cloud workspaces and the partition `rome`. The fundamentals deck says those two partition names point at the same nodes. This page does not choose.

Use the address in the welcome note. There is one login node. Your trainer sends a setup link. That link sets your password.

```bash
ssh YOUR_LOGIN@MANAGER
```

`module load 2025` loads EESSI 2025.06. `module load 2024` selects that same stack. There is no project budget on this cluster. `sacct` still reports core-seconds in `CPUTimeRAW`.

Whether mpiFileUtils is installed there is also still open. EESSI 2023.06 and 2025.06 do not provide it. Do not tell the room that the course cluster has it, and do not tell them that it is missing.

## The EESSI client, when you have no cluster

The software lesson also runs in the EESSI client container. Access is documented at <https://www.eessi.io/isc26-tutorial/getting-access/> and day-to-day use at <https://www.eessi.io/isc26-tutorial/usage/>.

You need Apptainer 1.0 or newer, with `--fusemount` support. This shell mounts the same repository the cluster uses. It does not give you Slurm.

```bash
mkdir -p "$HOME/eessi-work/var-lib-cvmfs" "$HOME/eessi-work/var-run-cvmfs" "$HOME/eessi-work/home"
export APPTAINER_BIND="$HOME/eessi-work/var-run-cvmfs:/var/run/cvmfs,$HOME/eessi-work/var-lib-cvmfs:/var/lib/cvmfs"
export APPTAINER_HOME="$HOME/eessi-work/home:/home/$USER"
apptainer shell --fusemount "container:cvmfs2 software.eessi.io /cvmfs/software.eessi.io" docker://ghcr.io/eessi/client:rocky8
```

Inside the container:

```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module load Python/3.13.5-GCCcore-14.3.0
python3 --version
```

`python3 --version` prints `Python 3.13.5`. The first launch downloads the image and can take a few minutes. The container has no `sbatch` and no `squeue`.
