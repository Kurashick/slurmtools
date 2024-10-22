#!/bin/bash
#============ Slurm Options ===========
#SBATCH -o path/to/example/output/%x.%j.out
#SBATCH -e path/to/example/output/%x.%j.err
#SBATCH -p gr10569b
#SBATCH -t 24:00:00
#SBATCH --rsc p=108:t=1:c=1:m=4G

#============ Shell Script ============
srun pw.x -nk 3 -nt 6 -nd 6 < ./espresso.pwi > ./espresso.pwo
# made by sh.py automatically
# 日時