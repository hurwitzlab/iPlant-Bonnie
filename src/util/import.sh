#!/usr/bin/sh

python2.7 import_feature.py -f features_BlastProDom -s feature.sql

for file in `ls feature_files/feature/*`
do
	 python2.7 import_feature.py -f $file
	 echo "$file data imported."
done

