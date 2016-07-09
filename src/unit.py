#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collegue import Collegue

class Unit(Collegue):
	"""単位の情報を持つクラス．

	example:
		{MB}, {kg->g}, {m/s}
	"""

	def __init__(self, ex_numer=None, numer=None, ex_denom=None, denom=None, token=None):
		""" Unitの初期化
		"""
		self.token = token
		self.ex_numer = ex_numer
		self.numer = numer
		self.ex_denom = ex_denom
		self.denom = denom

	def replace_tokens(self):
		"""
		"""
		tokens = [self.ex_numer, self.numer, self.ex_denom, self.denom]
		scopes = self.mediator.get_scopes()
		unit_manager = self.mediator.get_unit_manager()
		new_tokens = []
		for t in tokens:
			found_scope = scopes.peek().find_scope_of(t)
			if found_scope:
				unitx_obj = found_scope[t]
				new_tokens.append(unitx_obj.get_value())
			else:
				new_tokens.append(t)
		self.ex_numer, self.numer, self.ex_denom, self.denom = new_tokens
		return
	
	def remove_ex(self):
		"""
		"""
		self.ex_numer = self.ex_denom = None
	

	def is_empty(self):
		"""
		"""
		return self.ex_numer == self.numer == self.ex_denom == self.denom == None


	def notifyEasily(self, unit, opp_token):
		"""
		"""
		msg = "TypeError: unsupported operand for %s: unit '%s' and unit '%s'" % (opp_token.text, self.formal_str(), unit.formal_str())
		self.mediator.get_parser().notifyErrorListeners(msg, opp_token, Exception(msg))


	def add(self, unit, opp_token):
		"""
		<self> <operator> <unit>
		example:
			???{x/y} + ???{x/y}
		"""
		if self.numer == unit.numer and self.denom == unit.denom: return self
		elif self.is_empty(): return unit
		elif unit.is_empty(): return self
		else:
			self.notifyEasily(unit, opp_token)
	
	def subtract(self, unit, opp_token):
		"""
		"""
		self.add(unit, opp_token)


	def multiply(self, unit, opp_token):
		"""
		"""
		if self.numer == unit.denom: return Unit(numer=unit.numer)
		elif self.denom == unit.numer: return Unit(numer=self.numer)
		elif self.is_empty(): return unit
		elif unit.is_empty(): return self
		else:
			self.notifyEasily(unit, opp_token)

	def divide(self, unit, opp_token):
		"""
		"""
		if self.numer == unit.numer and self.denom == unit.denom: return Unit()
		elif (not self.denom) and self.numer == unit.numer: return Unit(numer=unit.denom)
		elif self.is_empty(): return unit
		elif unit.is_empty(): return self
		else:
			self.notifyEasily(unit, opp_token)

	def modulo(self, unit, opp_token):
		"""
		"""
		return self.divide(unit, opp_token)
	
	def equals(self, unit):
		""" 
		"""
		return self.numer == unit.numer and self.denom == unit.denom

	def formal_str(self):
		"""
		"""
		if self.numer and self.denom:
			return '{%s/%s}' % (self.numer, self.denom)
		elif self.numer and not self.denom:
			return '{%s}' % (self.numer)
		else:
			return ''

	def __unicode__(self):
		""" 値と変数を詳細に表示する．
		"""
		res = "<%s: {%s->%s/%s->%s}>" % (self.__class__.__name__, self.ex_numer, self.numer, self.ex_denom, self.denom)
		return res

	def __str__(self):
		""" Returns an encoded string of attributes."""
		return unicode(self).encode('utf-8')

	def __repr__(self):
		""" Returns a string of attributes."""
		return self.__str__()

	@classmethod
	def set_mediator(self, mediator):
		"""Sets a mediator for Mediator pattern of GoF."""
		self.mediator = mediator


def main():
	"""Run an example for a Unit class."""

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

	#left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	#print "%s * %s\t-> %s" % (left.formal_str(), right.formal_str(), left.multiply(right)) #error

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

	#left, right = Unit(None, u'km', None, u'時'), Unit(None, u'時', None, None)
	#print "%s / %s\t-> %s" % (left.formal_str(), right.formal_str(), left.divide(right)) #error

	return 0

if __name__ == '__main__':
	sys.exit(main())
