#!/bin/bash

# Set the partition where the job will run
#SBATCH --partition=htc

#SBATCH --gres=gpu:1 --constraint='gpu_gen:Kepler'

# Set the number of nodes requested (1 == not parallel, >1 == parallel)
#SBATCH --nodes=1

# Number of processor cores (i.e. tasks)
#SBATCH --ntasks-per-node=1

# Set max wallclock time
#SBATCH --time=120:00:00

# Array jobs (max of 1000 arrays per job)
#SBATCH --array=0-499

# Mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# Send mail to this address
#SBATCH --mail-user=19veronika97@gmail.com

module load intel-compilers
module load intel-mkl

WORKING_DIR=$PWD
RUNS_DIR=$WORKING_DIR/multiple_models

RUN_ID=$(($OFFSET + $SLURM_ARRAY_TASK_ID)) # $OFFSET is passed as a command line variable to this script and $SLURM_ARRAY_TASK_ID is given by #SBATCH --array=1-13
echo "Array ID (from 0 to 999):" $SLURM_ARRAY_TASK_ID
echo "Offset (in groups of 1000):" $OFFSET

cd $RUNS_DIR/model_${RUN_ID}; pwd # change to the right directory using $SLURM_ARRAY_TASK_ID
make clean
make cleanoutput
make FC=gfortran
echo "Starting run number" $RUN_ID
./SLAMSexecutable > logfile_${RUN_ID}

echo "Finished. Moving output files"
#moving the output files to the output folder 
mv out_control.bin out_stats_nClusters.bin out_stats_nParticles.bin out_flux_seafloor.bin out_flux.bin out_avgparticleatt_maintype_seafloor.bin out_avgparticleatt_maintype.bin out_avgparticleatt_sizeclass_seafloor.bin out_avgparticleatt_sizeclass.bin out_avgparticleatt_veloclass_seafloor.bin out_avgparticleatt_veloclass.bin out_sms.bin out_sms_annual.bin out_aux.bin out_cluster_i.bin out_cluster_r.bin logfile_${RUN_ID} $RUNS_DIR/all_outputs/model_output_${RUN_ID}
