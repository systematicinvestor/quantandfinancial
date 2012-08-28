# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from math import pow, floor, ceil, log
from quant.optimization import newton

class TVM:
	def __str__(self):
		return "n=%f, r=%f, pv=%f, pmt=%f, fv=%f" % (self.n, self.r, self.pv, self.pmt, self.fv)
	def __init__(self, n=0.0, r=0.0, pv=0.0, pmt=0.0, fv=0.0):
		self.n = float(n)
		self.r = float(r)
		self.pv = float(pv)
		self.pmt = float(pmt)
		self.fv = float(fv)
	def calc_pv(self):
		z = pow(1+self.r, -self.n)
		pva = self.pmt / self.r
		return -(self.fv*z + (1-z)*pva)
	def calc_fv(self):
		z = pow(1+self.r, -self.n)
		pva = self.pmt / self.r
		return -(self.pv + (1-z) * pva)/z
	def calc_pmt(self):
		z = pow(1+self.r, -self.n)
		return (self.pv + self.fv*z) * self.r / (z-1)
	def calc_n(self):
		pva = self.pmt / self.r
		z = (-pva-self.pv) / (self.fv-pva)
		return -log(z) / log(1+self.r)
	def calc_r(self):
		def function_fv(r, self):
			z = pow(1+r, -self.n)
			pva = self.pmt / r
			return -(self.pv + (1-z) * pva)/z
		return newton(function_fv, self, 5, self.fv, 1000, 0.0001) 		
			