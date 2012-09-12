# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

import io
import time
from quant.tvm import TVM

class Bond:
	epic = None
	desc = None
	couponRate = None	# quoted annually
	maturity = None		# payment frequency
	freq = None
	bid = None
	ask = None
	def __str__(self):
		return "epic=%s ttm=%f ytm=%f" % (self.epic, self.ttm(), self.calc_ytm())
	def ttm(self, localtime, daysInYear = 360): # in years
		delta = self.maturity - localtime
		return delta.days / daysInYear
	def mid(self):
		return (self.bid + self.ask) / 2
	def calc_ytm(self):
		tvm = TVM(self.ttm()*self.freq, 0, -self.mid(), self.couponRate/self.freq, 1) #semiannual payment
		try:
			return tvm.calc_r() * self.freq
		except Exception:
			return None

def getyieldcurve(bonds):
	out = []
	for b in bonds:
		t = b.ttm(), b.calc_ytm()
		out.append(t)		
	return out
	