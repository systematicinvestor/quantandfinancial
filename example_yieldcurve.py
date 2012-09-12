# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from datasources.bondscape import readfromfile
from structures.bond import getyieldcurve
from quant.tvm import TVM
from datetime import datetime
import scipy.interpolate

# get bonds
bonds = readfromfile('data/gilts_2012_06_13.csv')

#local time
localtime = datetime(2012,6,13)

# Calculated YTMs doesn't necessarily correspond to those quoted in data file (source: Bondscape.net), due to accrued interest
# and a fact that coupon payment are bound to some specific calendar date, not necessarily, one semiannually

# calculate yield curve
t, y = [], []
for b in bonds:
	ttm = (b.maturity - localtime).days / 360
	if ttm <= 0: continue
	ytm = TVM(ttm * b.freq, 0, -(b.ask+b.ask)/2, b.couponRate/b.freq, 1).calc_r() * b.freq
	t.append(ttm)
	y.append(ytm)

# interpolation
tNorm = [1/12, 3/12, 6/12, 1, 2, 3, 4, 5, 7, 8, 9, 10, 15, 20, 30]
yNorm = []
interp = scipy.interpolate.interp1d(t, y)
for t in tNorm:
	try:
		yNorm.append(float(interp(t)))
	except: # value is outside interpolation range
		yNorm.append(scipy.nan)

# bootstrapping, calculation of spot rates
for i in reversed(range(0, len(tNorm))):
	print(i, tNorm[i], yNorm[i])