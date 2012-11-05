# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

import datasources.google as google
from structures.quote import QuoteSeries
import random
import io
from numpy import array, std
from math import log, exp
from datetime import datetime

qs = QuoteSeries.loadfromfile('IVV', 'data/ivv_2012_11_04.csv')
prices = qs.getprices()
prices = prices[:-100]

# calculate daily logaritmic (continuously compounded) returns
returns = []
for i in range(0, len(prices)-1):
	r = log(prices[i] / prices[i-1])
	returns.append(r)
returns = array(returns)   	  # daily returns

# calculate daily and annualized volatility
vd = std(returns) 	# daily volatility
va = vd * 250**.5	# annualized volatility

class Side:
	CALL=0
	PUT=1

class Type:
	EUROPEAN=0
	AMERICAN=1

price = 30#prices[-1]			# current instrument price 
s = 29					# strike
side = Side.CALL		# side
type = Type.EUROPEAN 	# type
rf = .05				# risk-free rate
dy = .02				# dividend yield
tte = (datetime(2012,12,22) - datetime(2012,11, 4)).days
tte = 100 #todo
va = .1 #todo

n = 10							# binomial tree steps
tdelta = tte / (n * 365)		# calculate time delta of one step (as fraction of year)
u = exp(va * tdelta**.5)		# calculate up movement
d = 1/u							# calculate down movement
rfdelta = exp(rf * tdelta) - 1	# calculate rf delta
dydelta = exp(dy * tdelta) - 1  # calcilate dy delta
pu = (1 + rfdelta - dydelta - d) / (u - d)
pd = 1 - pu

# generate binomial tree
tree = []
for i in range(0, n+1):
	pr = price * d**(n-i) * u**i
	ov = max(0.0, pr-s) if side==Side.CALL else max(0.0, s-pr)
	tree.append((pr, ov))
	print((pr, ov))
print()
	
# reduce binomial tree
for i in range(n+1, 1, -1):
	treeNext = []
	for j in range(0, i-1):
		node_d, node_u = tree[j], tree[j+1]
		pr = node_d[0] / u
		ov = (node_d[1] * pd + node_u[1] * pu) / (1 + rfdelta)	
		treeNext.append((pr, ov))
		print((pr, ov))
	tree = treeNext
	print()