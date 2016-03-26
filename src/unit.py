#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Unit:
	""" 単位の情報を持つクラス．
		ex: {MB}, {kg->g}, {m/s}
	"""

	def __init__(self, ex_numer, numer, ex_denom, denom):
		""" Unitの初期化
		"""
		self.ex_numer = ex_numer
		self.numer = numer
		self.ex_denom = ex_denom
		self.denom = denom
	
	def formal_str(self):
		if self.numer and self.denom:
			return '{%s/%s}' % (self.numer, self.denom)
		elif self.numer and not self.denom:
			return '{%s}' % (self.numer)

	def __unicode__(self):
		""" 値と変数を詳細に表示する．
		"""
		res = "<%s: {%s->%s/%s->%s}>" % (self.__class__.__name__, self.ex_numer, self.numer, self.ex_denom, self.denom)
		return res

	def __str__(self):
		return unicode(self).encode('utf-8')

	def __repr__(self):
		return self.__str__()

def main():
	unit = Unit(u'分',u'時', None, None)
	print unit
	print unit.formal_str()
	unit = Unit(u'm',u'km', None, u'時')
	print unit
	print unit.formal_str()
	return 0

if __name__ == '__main__':
	sys.exit(main())
