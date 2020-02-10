#!/bin/bash
#PBS -l nodes=4:ppn=4
#PBS -l mem=5GB
#PBS -l walltime=1:00:00
#PBS -q iw-shared-6
#PBS -N environ_test
#PBS -o stdout
#PBS -e stderr
cd $PBS_O_WORKDIR

sparc -name sprc-calc
