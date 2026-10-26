---
title: Learner profiles
---

## Sam

Sam's program writes thousands of small output files, and Sam copies that directory with `cp -r`. The copy spends its time on metadata. The win is one archive, `sha256sum -c` printing `src.tar: OK`, and a stage script that copies the tree back to scratch before the job ends.
