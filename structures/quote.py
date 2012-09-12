# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# quantandfinancial.blogspot.com

from datetime import datetime
import io

class QuoteSeries:
	def __init__(self, name = None, data = None):
		self.name = name
		self.data = data if data != None else []
	def __str__(self):
		dateFromStr = datetime.strftime('%Y-%m-%d', self.data[0].date)
		dateToStr =   datetime.strftime('%Y-%m-%d', self.data[-1].date)
		return self.name + " : " + str(len(self.data)) + " quotes [" + dateFromStr + " - " + dateToStr + "], last "+str(self.data[-1].c)
	def getprices(self):
		array = []
		for quote in self.data:
			array.append(quote.c)
		return array
	@staticmethod
	def intersect(qs1, qs2):
		assert(type(qs1)==QuoteSeries and type(qs2)==QuoteSeries)
		set1, set2 = set(), set()
		for q in qs1.data: set1.add(q.date)
		for q in qs2.data: set2.add(q.date)
		set0 = set1 & set2
		qs1out, qs2out = QuoteSeries(qs1.name), QuoteSeries(qs2.name)
		for q in qs1.data:
			if q.date in set0:
				qs1out.data.append(q)
		for q in qs2.data:
			if q.date in set0:
				qs2out.data.append(q)
		if __debug__:
			assert(len(qs1out.data)==len(qs2out.data))
			for i in range(0, len(qs1out.data)):
				assert(qs1out.data[i].date==qs2out.data[i].date)
		return qs1out, qs2out
	def savetofile(self,filename):
		f = io.open(filename, "w")
		f.write('date, open, high, low, close, volume\n')
		for q in self.data:
			f.write(str(q.date)+","+str(q.o)+","+str(q.h)+","+str(q.l)+","+str(q.c)+","+str(q.v)+"\n")
		f.close()
			
class Quote:
	def __init__(self, date, o, h, l, c, v):
		self.date = date
		self.o = o
		self.h = h
		self.l = l
		self.c = c
		self.v = v
	def __str__(self):
		return "%s c=%f" % (datetime.strftime('%Y-%m-%d', self.date), self.c)