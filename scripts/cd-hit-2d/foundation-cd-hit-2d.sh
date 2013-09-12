INPUT=${inputSeqs}
CLUSTERS=${clusters} 
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
iget -fT "${CLUSTERS}"
wait
INPUT_F=$(basename ${INPUT})
CLUSTERS_F=$(basename ${CLUSTERS})

chmod a+x cd-hit-2d
cd-hit-2d -i "${INPUT_F}" -i2 "${CLUSTERS_F}" -o "${OUTNAME}"  -c "${IDTHRESHOLD}" -aS "${ALIGNCOVER}" -g "${ALGORITHM}" -n "${WORDLENGTH}" -d "${DESCLENGTH}" -T "${THREADS}" -M "${MEMORYLIMIT}" 
