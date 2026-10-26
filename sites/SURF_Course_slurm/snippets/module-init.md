```bash
module load 2025
module load {{remote.modules.python}}
```

`module load 2025` loads EESSI 2025.06. `module load 2024` selects that same stack and is the one you load before `QCG-PilotJob`. The names `2024` and `foss/2023a` also load the 2025.06 stack on this cluster, so older scripts keep working.
