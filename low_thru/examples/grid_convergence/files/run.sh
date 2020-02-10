#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l pmem=3GB
#PBS -l walltime=12:00:00
#PBS -q iw-shared-6
#PBS -N Convergence_Calc
#PBS -o stdout
#PBS -e stderr
cd $PBS_O_WORKDIR


module load anaconda3/4.2.0;source activate atm

export ABINIT_PP_PATH=/gpfs/pace1/project/chbe-medford/medford-share/data/pseudos/oncv_2015/psp_cut/

python run.py
