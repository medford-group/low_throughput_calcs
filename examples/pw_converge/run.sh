#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l pmem=3GB
#PBS -l walltime=12:00:00
#PBS -q iw-shared-6
#PBS -N Nitrogen Adsorption
#PBS -o stdout
#PBS -e stderr
cd $PBS_O_WORKDIR
source  /gpfs/pace1/project/chbe-medford/medford-share/envs/espresso-5.1.r11289-pybeef_ase3.14_cust_esp

python {sp}_build.py
python run.py
