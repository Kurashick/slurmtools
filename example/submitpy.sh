#!/bin/bash
#============ Slurm Options ===========
#SBATCH -o /home/b/b38622/develop/slurmtools/example/output/%x.%j.out
#SBATCH -e /home/b/b38622/develop/slurmtools/example/output/%x.%j.err
#SBATCH -p gr10569b
#SBATCH -t 24:00:00
#SBATCH --rsc p=1:t=1:c=1:m=4G

#============ Shell Script ============
srun python3.11 -u /home/b/b38622/develop/slurmtools/example/testase.py
# made by sh.py automatically
# 2024-10-22 19:21:33.590113