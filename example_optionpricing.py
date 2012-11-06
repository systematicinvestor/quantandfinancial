# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

import datasources.google as google
from structures.quote import QuoteSeries
import numpy
from math import log, exp
from datetime import datetime

CALL, PUT, EUROPEAN, AMERICAN = 100, 101, 102, 103

prices = QuoteSeries.loadfromfile('IVV', 'data/ivv_2012_11_06.csv').getprices()
prices = prices[:-30]

# calculate daily logaritmic (continuously compounded) returns
returns = []
for i in range(0, len(prices)-1):
	r = log(prices[i] / prices[i-1])
	returns.append(r)

# calculate daily and annualized volatility
volat_d = numpy.std(returns)	# daily volatility
volat = volat_d * 250**.5		# annualized volatility

side = CALL				# side
type = EUROPEAN 		# type
price = prices[-1]		# current instrument price 
strike = 140			# strike
riskfree = .0010		# risk-free rate, current 3m treasury yields, as of 2012/11/02
divyield = .0199		# dividend yield on S&P 500, as of 2012/11/02
tte = (datetime(2012,12,22) - datetime(2012,11, 6)).days

n = 8							# binomial tree steps
tdelta = tte / (n * 365)		# calculate time delta of one step (as fraction of year)
u = exp(volat * tdelta**.5)		# calculate up movement
d = 1/u							# calculate down movement
rf = exp(riskfree * tdelta) - 1	# calculate rf delta
dy = exp(divyield * tdelta) - 1  # calcilate dy delta
pu = (1 + rf - dy - d) / (u - d)
pd = 1 - pu

assert(side==CALL or side==PUT)
assert(type==AMERICAN or type==EUROPEAN)

# generate binomial tree
tree = []
print('Tree layer %i' % n)
for i in range(0, n+1):
	pr = price * d**i * u**(n-i)
	ov = max(0.0, pr-strike) if side==CALL else max(0.0, strike-pr)
	tree.append((pr, ov))
	print('Node Price %.3f, Option Value %.3f' %(pr, ov))
	
# reduce binomial tree
for i in range(n+1, 1, -1):
	treeNext = []
	print('Tree layer %i' % (i-1-1))
	for j in range(0, i-1):
		node_u, node_d = tree[j], tree[j+1]
		pr = node_d[0] / d
		ov = (node_d[1] * pd + node_u[1] * pu) / (1 + rf)	
		if type==AMERICAN:
			ov = max(ov, pr-strike if side==CALL else strike-pr)
		treeNext.append((pr, ov))
		print('Node Price %.3f, Option Value %.3f' %(pr, ov))
	tree = treeNext

