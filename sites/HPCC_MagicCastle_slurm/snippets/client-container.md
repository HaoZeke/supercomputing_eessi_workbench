The EESSI client container mounts the same repository and has no Slurm.

```bash
mkdir -p "$HOME/eessi-work/var-lib-cvmfs" "$HOME/eessi-work/var-run-cvmfs" "$HOME/eessi-work/home"
export APPTAINER_BIND="$HOME/eessi-work/var-run-cvmfs:/var/run/cvmfs,$HOME/eessi-work/var-lib-cvmfs:/var/lib/cvmfs"
export APPTAINER_HOME="$HOME/eessi-work/home:/home/$USER"
apptainer shell --fusemount "container:cvmfs2 software.eessi.io /cvmfs/software.eessi.io" docker://ghcr.io/eessi/client:rocky8
```

Inside the container:

```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
```

`sbatch` and `squeue` are not there.
