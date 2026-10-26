---
title: "Learner profiles"
---

## Idris

Idris runs a job that writes a large result, then copies that result into home because home is the directory the shell started in. The next job does the same. Home is 200 GiB on Snellius, and it is backed up, so the copies are expensive as well as large. A full quota then stops Idris editing the script that would have moved the data.

The win is a split. The source file stays in home. The 10 GB working file goes to scratch or to the job's `$TMPDIR`. The result that must be kept until the project ends goes to the project path, not to home. Idris can point at `ls -l` and say which of the three lifetimes matches which path: 14 days, the end of the job, the end of the project.
