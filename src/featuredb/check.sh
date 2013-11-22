#!/usr/bin/sh

for file in `ls feature_files/feature/*`
do
	 python2.7 check_data.py -f $file
	 echo "$file checked"
 done

