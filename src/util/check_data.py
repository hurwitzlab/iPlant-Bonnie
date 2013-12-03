#!/usr/bin/env python
import csv

from optparse import OptionParser
import FeatureApi

def main():

	parser = OptionParser()
	parser.add_option("-f", "--file", dest="ifile",
                  help="file to be imported", type="string")

	parser.add_option("-s", "--script", dest="script",
                  help="sql script to be executed", type="string")

	(options, args) = parser.parse_args()

	if options.ifile == None :
                raise TypeError('filename missing from command-line.')


	arr = list(csv.reader(open(options.ifile, 'rb'), delimiter='\t'))

	for i in arr:
        	if len(i) != 13:
                	print len(i)

if __name__ == "__main__":
    main()

