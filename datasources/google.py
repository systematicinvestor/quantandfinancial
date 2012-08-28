# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from structures.quote import Quote, QuoteSeries
import time
import urllib.request

def getquotes(symbol):
	url = "http://www.google.com/finance/historical?q=" + symbol + "&output=csv"
	page = str(urllib.request.urlopen(url).read())
	linecount = 0
	data = []
	for line in page.split("\\n"):
		linecount += 1
		entries = line.split(",")
		if len(entries) != 6 or linecount==1: continue
		quote = Quote(
			time.strptime(entries[0], '%d-%b-%y'),
			float(entries[1]),
			float(entries[2]),
			float(entries[3]),
			float(entries[4]),	
			int(entries[5]))
		data.append(quote)
	reversedIterator = reversed(data)
	return QuoteSeries(symbol, list(reversedIterator))
