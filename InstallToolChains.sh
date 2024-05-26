#!/bin/bash -l
#SBATCH --job-name=test-install-eb-modules
#SBATCH --output=out/test-install-eb-module-%j.out
#SBATCH --time=20:00:00
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --mem=0

module purge
export EASYBUILD_JOB_BACKEND=Slurm
print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
hash parallel 2>/dev/null && test $? -eq 0 || print_error_and_exit "Parallel is not installed on the system"

module load tools/EasyBuild/4.9.1

EBFILES=("foss-2023a.eb" "intel-2023a.eb")
mkdir -p logs

parallel -j 1 --verbose --joblog eb-joblog.log "srun -n1  -c 8 eb {} --robot --job --job-cores=8 --job-max-walltime=5 --job-backend-config=slurm --trace --accept-eula-for=Intel-oneAPI> logs/eb-log-{#}.log" ::: "${EBFILES[@]}"

echo 'Tasks are all runing now sq to see them'
