#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from collegue import Collegue
from constants import Constants

class DefinedFunction(Collegue):
	"""A Class for saving a infomation of defined function.
	
	Attributes:
		name: A string indicating function name.
		args: A list of string indicating function argument.
		ctx: An instance of ParserRuleContext of functionDeclaration RULE.
		_current_scope: A instance of Scope saving an instance of this class.
	"""

	def __init__(self, name, args, ctx, current_scope=None):
		"""Inits attributes of a DefinedFunction class. """
		self.name = name
		self.args = args
		self.ctx = ctx
		self._current_scope = current_scope


	def get_current_scope(self):
		"""Returns a current scope saving this class.

		Returns:
			A instance of Scope saving an instance of this class.
		"""
		return self._current_scope
	

	def __unicode__(self):
		"""Returns a string of attributes.

		Returns:
			A string of infomations of attributes.
		"""
		res = "<%s: %s(%s) ctx=%s>" % (self.__class__.__name__, self.name, self.args, self.ctx)
		return res


	def __str__(self):
		"""Returns an encoded string of attributes."""
		return unicode(self).encode('utf-8')


	def __repr__(self):
		"""Returns a string of attributes."""
		return self.__str__()


	@classmethod
	def set_mediator(self, mediator):
		"""Sets a mediator for Mediator pattern of GoF.
		
		Args:
			mediator: An instance of a EvalVisitor class inherited Mediator class.
		"""
		self.mediator = mediator

def main():
	"""Run an example for a DefinedFunction class.

	Advice:
		A value of 'ctx' should get from an argument of visitFunctionDeclaration(ctx).
	"""

	# Prepare
	from unitx_object import UnitXObject
	from unit_manager import UnitManager
	from scope_list import ScopeList
	from util import Util
	scopes = ScopeList()
	UnitXObject.unit_manager = UnitManager('data/unit_table.dat')
	UnitXObject.scopes = scopes
	scopes.new_scope()

	# Define variables
	current_scope = scopes.peek()
	x, y = UnitXObject(None,None,None,is_none=True), UnitXObject(None,None,None,is_none=True)
	current_scope['x'] = x
	current_scope['y'] = y
	current_scope['dfs'] = DefinedFunction('dfs', [['x', x], ['y', y], ['level', None]], ctx=None)

	# Output
	Util.dump(current_scope)
	scopes.del_scope()

	return Constants.EXIT_SUCCESS

if __name__ == '__main__':
	sys.exit(main())
