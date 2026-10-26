```bash
module load 2025
module load {{remote.modules.python}}
```

`module load 2025` selects the 2025 software stack on Snellius. In the EESSI client container, which has no site module named `2025`, source the init script instead:

```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
```
