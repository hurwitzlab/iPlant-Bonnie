#!/bin/bash
#SBATCH -J cd-hit-2d         # job name
#SBATCH -o cd-hit-2d.o%j     # output and error file name (%j expands to jobID)
#SBATCH -p development     # queue (partition) -- normal, development, etc.
#SBATCH -t 00:30:00        # run time (hh:mm:ss) - 1.5 hours
#SBATCH --mail-user=darren.boss@gmail.com
#SBATCH --mail-type=begin  # email me when the job starts
#SBATCH --mail-type=end    # email me when the job finishes
#SBATCH -N 1 -n 1  # one node and one task
#SBATCH
set -x

INPUT=/iplant/home/dboss/input.fa
CLUSTERS=/iplant/home/dboss/current-prot-universe.fa 
OUTNAME=/home1/02452/dboss/data/cdhit60
IDTHRESHOLD="0.6"
ALIGNCOVER="0.8"
ALGORITHM=1
WORDLENGTH=4
DESCLENGTH=0
THREADS=24
MEMORYLIMIT=45000

module purge
module load TACC
module swap intel gcc
module load irods

iinit Bc455XHraRJw
wait

#Copy from iRODS
iget -fT "${INPUT}"
iget -fT "${CLUSTERS}"
wait
INPUT_F=$(basename ${INPUT})
CLUSTERS_F=$(basename ${CLUSTERS})

/work/02452/dboss/cd-hit-4.6.1/cd-hit-2d -i "${INPUT_F}" -i2 "${CLUSTERS_F}" -o "${OUTNAME}"  -c "${IDTHRESHOLD}" -aS "${ALIGNCOVER}" -g "${ALGORITHM}" -n "${WORDLENGTH}" -d "${DESCLENGTH}" -T "${THREADS}" -M "${MEMORYLIMIT}" 
