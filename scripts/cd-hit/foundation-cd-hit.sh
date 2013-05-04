INPUT=${inputSeqs}
OUTNAME=${outputName}
IDTHRESHOLD=${idThreshold}
ALIGNCOVER=${alignCover}
ALGORITHM=${algorithm}
WORDLENGTH=${wordLength}
DESCLENGTH=${descLength}
THREADS=${threads}
MEMORYLIMIT=${memoryLimit}

#Copy from iRODS
iget -fT "${INPUT}"
wait
INPUT_F=$(basename ${INPUT})

chmod a+x cd-hit
cd-hit -i "${INPUT_F}" -o "${OUTNAME}"  -c "${IDTHRESHOLD}" -aS "${ALIGNCOVER}" -g "${ALGORITHM}" -n "${WORDLENGTH}" -d "${DESCLENGTH}" -T "${THREADS}" -M "${MEMORYLIMIT}" 
