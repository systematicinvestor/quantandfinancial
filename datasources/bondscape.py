# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from bond import Bond, yield_curve
import bond
import io
import time
import quant
	
def read_from_file(filename):
	f = io.open(filename, 'r')
	data = f.read()
	bonds = []
	i = 0
	for line in data.split('\n'):
		i += 1
		if (i==1): continue
		entries = line.split(',')
		if (len(entries) != 9): continue
		b = Bond()
		b.freq = 2
		b.epic = entries[0]
		b.desc = entries[1]
		b.couponRate = float(entries[2]) / 100.0
		b.maturity = time.strptime(entries[3], '%d-%b-%y')
		b.bid = float(entries[4]) / 100
		b.ask = float(entries[5]) / 100
		bonds.append(b)
	return bonds
	
bonds = read_from_file('gilts_2012_06_13.csv')

for b in bonds:
	print(b)
	
for x in [1/12, 3/12, 6/12, 9/12, 1, 2, 3, 5, 10, 15, 20, 30, 50]:
	print(x, quant.interpolate(yield_curve(bonds), x))