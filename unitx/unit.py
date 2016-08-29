#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collegue import Collegue
from constants import Constants

class Unit(Collegue):
	"""A class which has an infomation of a unit.

	And this class can calculate between units by a function
	which this class has. 

	Attributes:
		ex_numer: A string indicating a numer of unit which used in the past.
		numer: A string indicating a current numer.
		ex_denom: A string indicating a denom of unit which used in the past.
		denom: A string indicating a current denom.
		token: An instance of Token class indicating the head of a unit statement.
	Examples:
		{MB}, {kg->g}, {m/s}, {km->m}, {km->m/s->h}
		A data structure: { <ex_numer> -> <numer> / <ex_denom> -> <denom> }
	"""

	def __init__(self, ex_numer=None, numer=None, ex_denom=None, denom=None, token=None):
		"""Inits attributes of a Unit class."""
		self.token = token
		self.ex_numer = ex_numer
		self.numer = numer
		self.ex_denom = ex_denom
		self.denom = denom

	def replace_tokens(self):
		"""Replaces unit tokens to new unit tokens by finding in scopes."""
		tokens = [self.ex_numer, self.numer, self.ex_denom, self.denom]
		new_tokens = []
		for t in tokens:
			found_scope = self.mediator.get_scopes().peek().find_scope_of(t)
			if found_scope:
				unitx_obj = found_scope[t]
				new_tokens.append(unitx_obj.get_value())
			else:
				new_tokens.append(t)
		self.ex_numer, self.numer, self.ex_denom, self.denom = new_tokens
		return
	
	def remove_ex(self):
		"""Removes varibles of ex_numer and ex_denom which don't need
			for displaying on CLI.
		"""
		self.ex_numer = self.ex_denom = None
		return

	def is_empty(self):
		"""Returns whether attributes of Unit are an empty.

		Returns:
			A bool indicating whether attributes of Unit are an empty.
		"""
		return self.ex_numer == self.numer == self.ex_denom == self.denom == None


	def __notifyEasily(self, unit, opp_token):
		"""Notify an error(notifyErrorListeners) easily.

		Args:
			self: An instance indicating a Unit class which probably has an error.
			unit: An instance indicating a Unit class which probably has an error.
			opp_token: An instance indicating a Token class reporting an error
				on the listener(EvalErrorListener).
		Raises:
			TypeError: An error occurred by a difference of a unit type.
		"""
		msg = Constants.TYPE_ERR_UNSUPPORTED_UNIT % (opp_token.text, self.formal_str(), unit.formal_str())
		self.mediator.get_parser().notifyErrorListeners(msg, opp_token, Exception(msg))
		return


	def add(self, unit, opp_token):
		"""Returns a unit added self and unit.

		Args:
			self: An instance indicating a Unit class.
			unit: An instance indicating a Unit class.
			opp_token: An instance indicating a Token class reporting an error
				on the listener(EvalErrorListener).
		Examples:
			<self> + <unit> -> <result>
			{km} + {} -> {km}
			{km} + {km} -> {km}
			{km/s} + {km/s} -> {km/s}
		"""
		if self.numer == unit.numer and self.denom == unit.denom: return self
		elif self.is_empty(): return unit
		elif unit.is_empty(): return self
		else:
			self.__notifyEasily(unit, opp_token)
			return
	

	def subtract(self, unit, opp_token):
		"""Returns a unit subtracted self and unit.

		Args:
			self: An instance indicating a Unit class.
			unit: An instance indicating a Unit class.
			opp_token: An instance indicating a Token class reporting an error
				on the listener(EvalErrorListener).
		Examples:
			<self> - <unit> -> <result>
			{km} - {} -> {km}
			{km} - {km} -> {km}
			{km/s} - {km/s} -> {km/s}
		"""
		return self.add(unit, opp_token)


	def multiply(self, unit, opp_token):
		"""Returns a unit multiplied self and unit.

		Args:
			self: An instance indicating a Unit class.
			unit: An instance indicating a Unit class.
			opp_token: An instance indicating a Token class reporting an error
				on the listener(EvalErrorListener).
		Examples:
			<self> * <unit> -> <result>
			{km} * {} -> {km}
			{km/s} * {s} -> {km}
		"""
		if self.numer == unit.denom: return Unit(numer=unit.numer)
		elif self.denom == unit.numer: return Unit(numer=self.numer)
		elif self.is_empty(): return unit
		elif unit.is_empty(): return self
		else:
			self.__notifyEasily(unit, opp_token)
			return


	def divide(self, unit, opp_token):
		"""Returns a unit divided self and unit.

		Args:
			self: An instance indicating a Unit class.
			unit: An instance indicating a Unit class.
			opp_token: An instance indicating a Token class reporting an error
				on the listener(EvalErrorListener).
		Examples:
			<self> / <unit> -> <result>
			{km} / {km} -> {}
			{km} / {s} -> {km/s}
			{km} / {km/s} -> {s}
		"""
		if self.numer == unit.numer and self.denom == unit.denom: return Unit()
		elif (not self.denom) and self.numer == unit.numer: return Unit(numer=unit.denom)
		elif self.is_empty(): return unit
		elif unit.is_empty(): return self
		else:
			self.__notifyEasily(unit, opp_token)
			return


	def modulo(self, unit, opp_token):
		"""Returns a unit calculated a modulo of self and unit.

		Args:
			self: An instance indicating a Unit class.
			unit: An instance indicating a Unit class.
			opp_token: An instance indicating a Token class reporting an error
				on the listener(EvalErrorListener).
		Examples:
			<self> % <unit> -> <result>
			{km} % {km} -> {}
			{km} % {s} -> {km/s}
			{km} % {km/s} -> {s}
		"""
		return self.divide(unit, opp_token)
	

	def equals(self, unit):
		"""Returns whether self unit equals a unit of arguments.
		
		Returns:
			A bool indicating whether self unit equals a unit of arguments.
		"""
		return self.numer == unit.numer and self.denom == unit.denom


	def formal_str(self):
		"""Returns a formal string displaying on CLI.

		Returns:
			A string displaying on CLI.
		"""
		if self.numer and self.denom:
			return '{%s/%s}' % (self.numer, self.denom)
		elif self.numer and not self.denom:
			return '{%s}' % (self.numer)
		else:
			return ''


	def __unicode__(self):
		"""Returns a string of attributes.

		Returns:
			res: A string of attributes infomations.
		"""
		res = "<%s: {%s->%s/%s->%s}>" % (self.__class__.__name__, self.ex_numer, self.numer, self.ex_denom, self.denom)
		return res

	def __str__(self):
		"""Returns an encoded string of attributes.

		Returns:
			An encoded string of attributes.
		"""
		return unicode(self).encode('utf-8')

	def __repr__(self):
		"""Returns a string of attributes.

		Returns:
			A string of a result of a __str__() function.
		"""
		return self.__str__()

	@classmethod
	def set_mediator(self, mediator):
		"""Sets a mediator for Mediator pattern of GoF.
		
		Args:
			mediator: An instance of a EvalVisitor class inherited Mediator class.
		"""
		self.mediator = mediator
		return


def main():
	"""Run an example for a Unit class."""

	#
	# Checks printing a Unit object.
	#
	print Unit(u'分', u'時', None, None)
	print Unit(u'm', u'km', None, u'時')

	#
	# add() demo
	#
	print '-' * 10
	opp_token = None
	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	print "%s + %s -> %s" % (left.formal_str(), right.formal_str(), left.add(right, opp_token).formal_str())

	#
	# subtract() demo
	#
	print '-' * 10
	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	print "%s - %s -> %s" % (left.formal_str(), right.formal_str(), left.subtract(right, opp_token).formal_str())

	#
	# multiply() demo
	#
	print '-' * 10
	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'時', None, None)
	print "%s * %s -> %s" % (left.formal_str(), right.formal_str(), left.multiply(right, opp_token).formal_str())

	left, right = Unit(None, u'km', None, None), Unit(None, None, None, None)
	print "%s * %s -> %s" % (left.formal_str(), right.formal_str(), left.multiply(right, opp_token).formal_str())

	left, right = Unit(None, None, None, None), Unit(None, u'km', None, u'時')
	print "%s * %s -> %s" % (left.formal_str(), right.formal_str(), left.multiply(right, opp_token).formal_str())

	#left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	#print "%s * %s -> %s" % (left.formal_str(), right.formal_str(), left.multiply(right, opp_token)) #error

	#
	# divide() demo
	#
	print '-' * 10
	left, right = Unit(None, u'km', None, None), Unit(None, u'km', None, u'時')
	print "%s / %s -> %s" % (left.formal_str(), right.formal_str(), left.divide(right, opp_token).formal_str())

	left, right = Unit(None, u'km', None, u'時'), Unit(None, u'km', None, u'時')
	print "%s / %s -> %s" % (left.formal_str(), right.formal_str(), left.divide(right, opp_token).formal_str())

	left, right = Unit(None, u'km', None, None), Unit(None, u'km', None, None)
	print "%s / %s -> %s" % (left.formal_str(), right.formal_str(), left.divide(right, opp_token).formal_str())

	left, right = Unit(None, u'km', None, None), Unit(None, None, None, None)
	print "%s / %s -> %s" % (left.formal_str(), right.formal_str(), left.divide(right, opp_token).formal_str())

	#left, right = Unit(None, u'km', None, u'時'), Unit(None, u'時', None, None)
	#print "%s / %s -> %s" % (left.formal_str(), right.formal_str(), left.divide(right, opp_token)) #error

	return Constants.EXIT_SUCCESS


if __name__ == '__main__':
	sys.exit(main())
