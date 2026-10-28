# Start with Open OnDemand

Use the course cluster in your browser. Your trainer supplies the portal address, username and private account-setup link. Each person uses their own account. No Snellius CUA account or SSH client is required.

## Set up and sign in

1. Open your own setup link privately, follow its password instructions and save your password. A consumed setup link is not the login page.
2. Open the course portal from your welcome note and sign in. Complete any authentication prompt shown for your account.
3. Open **Clusters**, then the course shell. Keep this terminal in one tab and this lesson in another.
4. Run the commands below. Check that the username is yours and identify the login node.

```bash
whoami
hostname
pwd
mkdir -p "$HOME/hpc-course"
cd "$HOME/hpc-course"
sinfo
```

Ask the trainer privately about access problems. Never share passwords or account-setup links. An existing password remains usable after its setup link expires.

## Files, terminal and applications

**Files**, then **Home Directory**, lets you upload scripts, read output and download results. The **Clusters** terminal provides the same account and files. It starts on the shared login node: use Slurm to run computations on compute nodes.

**Interactive Apps** offers Jupyter, VS Code and the desktop. Choose a small CPU request and a short duration, launch, wait for the session to run, then connect. Stop it from **My Interactive Sessions** when finished. A pending session is waiting for resources; do not submit duplicates. These applications are optional for the first batch job.

## Use your prepared exercise directory

The Introduction attendees already have the audited runnable exercises and QCG input archive in their own home directories. Start here in the browser terminal:

```bash
cd "$HOME/introduction-to-supercomputing/course-module-fundamentals-of-hpc/hands-on"
```

Keep your work in this directory. Downloading or cloning another copy is optional.

## Optional: download a separate classroom copy

The upstream changes are under review. Use the trainer's fork and classroom branch to match the slides:

```bash
git clone --branch course/maastricht-20261028 --single-branch \
  https://github.com/HaoZeke/introduction-to-supercomputing.git \
  "$HOME/introduction-to-supercomputing-class"
cd "$HOME/introduction-to-supercomputing-class/course-module-fundamentals-of-hpc/hands-on"
```

Keep any existing exercise directory; use the new directory shown above. You can also [download the classroom source archive](https://github.com/HaoZeke/introduction-to-supercomputing/archive/refs/heads/course/maastricht-20261028.zip) and unpack it through Files.

The website's additional exercises live in the [Workbench repository](https://github.com/HaoZeke/supercomputing_eessi_workbench). Their paths begin with lessons; the slide checkout uses course-module directories. Follow the path printed in your exercise.

## First batch job

```bash
sbatch --partition=rome --cpus-per-task=1 python.sh
squeue -u "$USER"
```

Save the job number printed by sbatch. Once the job finishes, read its slurm-JOBID.out file, replacing JOBID with that number. Expect a compute hostname and sum: 499999500000. The output is also accessible through Files.

## Software and storage

EESSI supplies the shared software stack. The course CernVM-FS repository supplies site tools and teaching material. Follow each exercise's explicit module instructions; year aliases are compatibility names, not software versions. CPU jobs use the rome partition. Scratch is temporary; download the results you need to retain.

## Other environments

[Snellius access documentation](https://servicedesk.surf.nl/wiki/display/WIKI/Access+to+Snellius) and the [EESSI client container](https://www.eessi.io/isc26-tutorial/getting-access/) support independent study. The container has no Slurm scheduler. Neither is required for this classroom path.
