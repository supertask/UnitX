#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collegue import Collegue
from defined_function import DefinedFunction

class Stdlib(Collegue):
	"""A built-in(standard) library) in UnitX.
	
	
	"""

	def __init__(self):
		"""Inits ."""
		self.func_names = {'expect': [[],[]]}
		self.funcs = [
			DefinedFunction(name='expect', defined_args=[['l',None],['r',None]], func_p=self.expect)
		]

	def expect(self, args, func_obj):
		"""
		Args:
			args: A list of instances of UnitXObject.
		"""
		
		l, r = args
		is_match = l.get_value() == r.get_value() and l.unit.equals(r.unit)
		if not is_match:
			msg = "Debug: '%s' didn't coincide with '%s'." % (l.get_unit_value(), r.get_unit_value())
			self.mediator.get_parser().notifyErrorListeners(msg, func_obj.token, Exception(msg))

	def r(self, args, func_obj):
		"""
		Args:
			args: A list of instances of UnitXObject.
			func_obj: An instance of UnitXObject indicated a function.
		Returns:
			range: A list of instances of UnitXObject.
		"""
		
		l, r = args
		is_match = l.get_value() == r.get_value() and l.unit.equals(r.unit)
		if not is_match:
			msg = "Debug: '%s' didn't coincide with '%s'." % (l.get_unit_value(), r.get_unit_value())
			self.mediator.get_parser().notifyErrorListeners(msg, func_obj.token, Exception(msg))

	def set_mediator(self, mediator):
		"""Sets a mediator for Mediator pattern of GoF.
		
		Args:
			mediator: An instance of a EvalVisitor class inherited Mediator class.
		"""
		self.mediator = mediator

def main():
	stdlib = Stdlib()
	stdlib.expect([a,b])
	#for func_name in stdlib.func_names:
	#	func_p = getattr(stdlib, func_name)
			

if __name__ == '__main__':
	sys.exit(main())
