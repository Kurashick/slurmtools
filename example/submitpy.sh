#!/bin/bash
#============ Slurm Options ===========
#SBATCH -o path/to/example/output/%x.%j.out
#SBATCH -e path/to/example/output/%x.%j.err
#SBATCH -p gr10569b
#SBATCH -t 24:00:00
#SBATCH --rsc p=1:t=1:c=1:m=4G

#============ Shell Script ============
srun python3.11 -u path/to/example/testase.py
# made by sh.py automatically
# 日時