#!/usr/bin/env python
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

	api = FeatureApi.FeatureApi()
	
	if options.script != None :
		api.create_table(options.script)
	api.import_file(options.ifile)

if __name__ == "__main__":
    main()

 
