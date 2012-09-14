# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from datasources.bondscape import readfromfile
from structures.bond import getyieldcurve
from quant.tvm import TVM
from datetime import datetime
import scipy.interpolate
from math import floor, ceil

# get bonds
bonds = readfromfile('data/gilts_2012_06_13.csv')

#local time
localtime = datetime(2012,6,13)

# Calculated YTMs doesn't necessarily correspond to those quoted in data file (source: Bondscape.net), due to accrued interest
# and a fact that coupon payment are bound to some specific calendar date, not necessarily, one semiannually

# calculate yield curve
tr, yr = [], []
for b in bonds:
	ttm = (b.maturity - localtime).days / 360
	if ttm <= 0: continue
	ytm = TVM(ttm * b.freq, 0, -(b.ask+b.ask)/2, b.couponRate/b.freq, 1).calc_r() * b.freq
	tr.append(ttm)
	yr.append(ytm)

print('Raw yield curve')
for i in range(0, len(tr)):
	print("%.2f\t%.2f%%" % (tr[i], 100*yr[i]))
	
# interpolation
t = list(i/2 for i in range(1,21))
y = []
interp = scipy.interpolate.interp1d(tr, yr)
for i in tr:
	try:
		y.append(float(interp(i)))
	except: # value is outside interpolation range
		y.append(scipy.nan)

print('Interpolated yield curve')
for i in range(0, len(t)):
	print("%.2f\t%.2f%%" % (t[i], 100*y[i]))
		
# bootstrapping
s = []
for i in range(0, len(t)):	#calculate i-th spot rate	
	sum = 0
	for j in range(0, i): #by iterating through 0..i
		#print('	j=%i'%j)
		sum += y[i] / (1 + s[j])**t[j]
	value = ((1+y[i]) / (1-sum))**(1/t[i]) - 1
	s.append(value)
	#print('s[%i]=%f'%(i,value))
		
print('Swap rates')
for i in range(0, len(t)):
	print("%.2f\t%.2f%%" % (t[i], 100*s[i]))
	
# reverse check
print('Reverse checck')
for i in range(0, len(t)):
	sum = 0
	ytm = y[i]
	for j in range(0, i):
		sum += ytm / (1+s[j])**t[j]
	sum += (1+ytm) / (1+s[i])**t[i]
	print("%.2f\t%.2f" % (t[i], sum))
