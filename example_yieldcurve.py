# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from datasources.bondscape import readfromfile
from structures.bond import getyieldcurve
from quant.tvm import TVM
from datetime import datetime
import scipy.interpolate
from math import floor, ceil
from quant.optimization import newton
import io

#local time
localtime = datetime(2012,6,13)

# R calculation
def calculate_bond_yield(self):
	def function_fv(r, self):
		z = pow(1+r, -self.n)
		m = pow(1+r, -self.n%1) # discount factor to align annuity to calendar coupon payments
		accrued = (1-self.n%1) * self.pmt
		pv = self.pv
		pmt = self.pmt
		fv = -(pv + (1-z) * (pmt / r))/z
		#fv = pmt/r + (pv - pmt*m/r)/z
		#fv = pmt/r - 1/z*(pmt/r/m + pv) + accrued
		return fv
	r = newton(f=function_fv, fArg=self, x0=.05, y=self.fv, maxIter=1000, minError=0.0001) 		
	return r


#calculate yield curve
# Calculated YTMs doesn't necessarily correspond to those quoted in data file (source: Bondscape.net), due to accrued interest
# and a fact that coupon payment are bound to some specific calendar date, not necessarily, one semiannually
tr, yr = [], []
for b in readfromfile('data/gilts_2012_06_13.csv'):
	ttm = (b.maturity - localtime).days / 360
	if ttm <= 0: continue
	tvm = TVM(n=ttm*b.freq, pv=-(b.bid+b.ask)/2, pmt=b.couponRate/b.freq, fv=1)
	ytm = calculate_bond_yield(tvm) * b.freq
	tr.append(ttm)
	yr.append(ytm)

#tr, yr, i = [], [], 0
#for line in io.open('data/gilts_2012_06_13.csv').read().split('\n'):
#	i+=1
#	if i==1: continue
#	entries = line.split(',')
#	if (len(entries) != 9): continue
#	ttm, ytm = (datetime.strptime(entries[3], '%d-%b-%y') - localtime).days / 360 , float(entries[8]) / 100
#	tr.append(ttm), yr.append(ytm)

print('Raw yield curve')
for i in range(0, len(tr)):
	print("%.2f\t%.2f%%" % (tr[i], 100*yr[i]))
	
exit()	
	
# interpolation
t = list(i/2 for i in range(1,21))
y = []
interp = scipy.interpolate.interp1d(tr, yr)
for i in t:
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
		sum += y[i] / (1 + s[j])**t[j]
	value = ((1+y[i]) / (1-sum))**(1/t[i]) - 1
	s.append(value)
	#print('s[%i]=%f'%(i,value))
		
print('Swap rates')
for i in range(0, len(t)):
	print("%.2f\t%.2f%%" % (t[i], 100*s[i]))
	
# reverse check
print('Reverse check')
for i in range(0, len(t)):
	sum = 0
	ytm = y[i]
	for j in range(0, i):
		sum += ytm / (1+s[j])**t[j]
	sum += (1+ytm) / (1+s[i])**t[i]
	print("%.2f\t%.2f" % (t[i], sum))
