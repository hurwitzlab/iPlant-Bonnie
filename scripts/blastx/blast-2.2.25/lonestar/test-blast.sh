#!/bin/bash
 
# These are needed to run the app test in the queue on your system
#$ -V
#$ -cwd
#$ -N  blast-api
#$ -j  y
#$ -o  $JOB_NAME.o$JOB_ID
#$ -pe 1way 12 
#$ -q  development
#$ -A  TG-OCE130020 
#$ -l  h_rt=00:30:00

#input 
INPUT=/iplant/home/dboss/query1.fa
#blastdbs
BLASTDBS=/scratch/projects/tacc/iplant/SIMAP/fileshare.csb.univie.ac.at/simap/sequences.fa
PROCESSORS=12
TYPE=blastx
OUTPUT=blastout.0
DESCRIPTIONS=10
ALN=10
EVAL=1e-3

# Unpack the bin.tgz file containing samtools binaries
# If you are relying entirely on system-supplied binaries or the modules
# system, you don't need this bit.
tar -xvf bin.tgz

# Fetch data from iPlant Data Store
module load iRODS
iget -fT $INPUT .
INPUT_F=$(basename ${INPUT})
export BLASTDB=/scratch/projects/tacc/iplant/SIMAP/fileshare.csb.univie.ac.at/simap/
bin/blastall -a $PROCESSORS -p $TYPE -i $INPUT_F -o $OUTPUT -v $DESCRIPTIONS -b $ALN -d $BLASTDBS -e $EVAL

# Now, delete the bin/ directory
rm -rf bin
