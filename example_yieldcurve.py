# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from datasources.bondscape import readfromfile
from structures.bond import getyieldcurve

curve = getyieldcurve(readfromfile('data/gilts_2012_06_13.csv'))

import numpy



print(curve)
