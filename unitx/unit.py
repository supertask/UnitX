#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Unit:
	""" 単位の情報を持つクラス．
		ex: {MB}, {kg->g}, {m/s}
	"""

	def __init__(self, ex_numer=None, numer=None, ex_denom=None, denom=None):
		""" Unitの初期化
		"""
		self.ex_numer = ex_numer
		self.numer = numer
		self.ex_denom = ex_denom
		self.denom = denom
	
	def add(self, unit):
		if self.numer == unit.numer and self.denom == unit.denom: return self
		else: return None #error
	
	def subtract(self, unit):
		if self.numer == unit.numer and self.denom == unit.denom: return self
		else: return None #error

	def multiply(self, unit):
		if self.numer == unit.denom: return Unit(numer=unit.numer)
		elif self.denom == unit.numer: return Unit(numer=self.numer)
		elif not self.numer and not self.denom: return unit
		elif not unit.numer and not unit.denom: return self
		else: return None #error

	def divide(self, unit):
		if self.numer == unit.numer and self.denom == unit.denom: return Unit()
		elif (not self.denom) and self.numer == unit.numer: return Unit(numer=unit.denom)
		elif not self.numer and not self.denom: return unit
		elif not unit.numer and not unit.denom: return self
		else: return None #error

	def formal_str(self):
		if self.numer and self.denom:
			return '{%s/%s}' % (self.numer, self.denom)
		elif self.numer and not self.denom:
			return '{%s}' % (self.numer)
		else:
			return '{}'

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
	print Unit(u'分', u'時', None, None)
	print Unit(u'm', u'km', None, u'時')

	#
	# add() demo
	#
	print '-' * 10
	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	print "%s + %s\t-> %s" % (left.formal_str(), right.formal_str(), left.add(right).formal_str())

	#
	# subtract() demo
	#
	print '-' * 10
	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	print "%s - %s\t-> %s" % (left.formal_str(), right.formal_str(), left.subtract(right).formal_str())

	#
	# multiply() demo
	#
	print '-' * 10
	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'時', None, None)
	print "%s * %s\t-> %s" % (left.formal_str(), right.formal_str(), left.multiply(right).formal_str())

	left, right = Unit(None, u'km', None, None), Unit(None, None, None, None)
	print "%s * %s\t-> %s" % (left.formal_str(), right.formal_str(), left.multiply(right).formal_str())

	left, right = Unit(None, None, None, None), Unit(None, u'km', None, u'時')
	print "%s * %s\t-> %s" % (left.formal_str(), right.formal_str(), left.multiply(right).formal_str())

	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	print "%s * %s\t-> %s" % (left.formal_str(), right.formal_str(), left.multiply(right)) #error

	#
	# divide() demo
	#
	print '-' * 10
	left, right = Unit(None, u'km', None, None), Unit(None, u'km', None, u'時')
	print "%s / %s\t-> %s" % (left.formal_str(), right.formal_str(), left.divide(right).formal_str())

	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	print "%s / %s\t-> %s" % (left.formal_str(), right.formal_str(), left.divide(right).formal_str())

	left, right = Unit(None, u'km', None, None), Unit(None, u'km', None, None)
	print "%s / %s\t-> %s" % (left.formal_str(), right.formal_str(), left.divide(right).formal_str())

	left, right = Unit(None, u'km', None, None), Unit(None, None, None, None)
	print "%s / %s\t-> %s" % (left.formal_str(), right.formal_str(), left.divide(right).formal_str())

	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'時', None, None)
	print "%s / %s\t-> %s" % (left.formal_str(), right.formal_str(), left.divide(right)) #error

	return 0

if __name__ == '__main__':
	sys.exit(main())
