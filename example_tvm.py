# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from quant.tvm import TVM

pmt = TVM(n=25*12, r=.04/12, pv=500000, fv=0).calc_pmt()
print("Payment = %f" % pmt)