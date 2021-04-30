#!/bin/bash
#SBATCH --account=<account>
#SBATCH --partition=<partition>
#SBATCH --ntasks=<ntasks>
#SBATCH --nodes=<nodes>
#SBATCH --time=<walltime>
#SBATCH --job-name=<jobname>
#SBATCH --output=<logdir>/%A.%a.out

## Cassandra has been tested with OpenMPI 3.1.0 and
## python/anaconda 3.6.4

source /etc/profile.d/modules.sh >& /dev/null
module load gcc/8.1.0
module load python/anaconda3.6
source /share/apps/python/anaconda3.6/etc/profile.d/conda.sh
module load R/3.4.3
module load intel

echo "Started at $(date)"
echo "nodes: $SLURM_JOB_NODELIST"

python -m rpy2.situation

tid=$SLURM_ARRAY_TASK_ID

# NOTICE:  Since I am only running 1 combination of model and rcp for 1 climate field each
#    task (fldgen setting `ngrid=1`), the following should be
#    executed:  `sbatch --array=0-39 <script>`

config="<cassconfigdir>/<model>_<scenario>_${tid}.cfg"
logdir="<casslogdir>/<model>_<scenario>_${tid}"
cassandra=<cassmainscript>

echo "mpirun -np 3 $cassandra --mp -v -l $logdir $config"

mpirun -np 3 $cassandra --mp -v -l $logdir $config

echo "Ended at $(date)"
