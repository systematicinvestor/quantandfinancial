# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

from datetime import datetime
import urllib.request
import io
import zipfile
import sys
from xml.dom import minidom
from datasources.worldbank import get_indicators

def parse_argv(argv):
	if len(argv)<3:
		print("Usage: <program.py> output_file indicator1 [indicator2] ..")
		exit(1)
	outputFile = argv[1]
	indicators = argv[2:]
	return outputFile, indicators
	
outputFile, indicators = parse_argv(sys.argv)	
	
print(indicators)	
	
print("Output file: %s" % outputFile)		
f = io.open(outputFile, 'w')

f.write("%s,%s,%s,%s,%s,%s\n" % ("CountryId", "CountryName", "IndicatorId", "IndicatorName", "Year", "Value"))
for row in get_indicators(indicators):
	f.write("%s,%s,%s,%s,%s,%s\n" % row)
	
f.close()