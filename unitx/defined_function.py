#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from collegue import Collegue

class DefinedFunction(Collegue):
	""" A Class for saving a info of defined function.
	
	Attributes:
		name: A string indicating function name.
		args: A list of string indicating function argument.
		ctx: An instance of ParserRuleContext of functionDeclaration RULE.
		current_scope: A instance of Scope saving an instance of this class.
	"""

	def __init__(self, name, args, ctx, current_scope=None):
		""" Inits DefinedFunction. """
		self.name = name
		self.args = args
		self.ctx = ctx
		self._current_scope = current_scope

	def get_current_scope(self):
		""" Returns a current scope saving this class.
			Returns:
				A instance of Scope saving an instance of this class.
		"""
		return self._current_scope
	
	def __unicode__(self):
		""" Outputs attributes bound by this class.
		"""
		res = "<%s: %s(%s) ctx=%s>" % (self.__class__.__name__, self.name, self.args, self.ctx)
		return res

	def __str__(self):
		return unicode(self).encode('utf-8')

	def __repr__(self):
		return self.__str__()

	@classmethod
	def set_mediator(self, mediator):
		self.mediator = mediator

def main():
	""" A example code.

		A value of 'func_name' should get by using visitFormalParameters(ctx).
		Also, a value of 'ctx' should get from argument of visitFunctionDeclaration(ctx).
	"""
	# Prepare part
	from unitx_object import UnitXObject
	from unit_manager import UnitManager
	from scope_list import ScopeList
	from util import Util
	scopes = ScopeList()
	UnitXObject.unit_manager = UnitManager('data/unit_table.dat')
	UnitXObject.scopes = scopes
	scopes.new_scope()

	current_scope = scopes.peek()
	x, y = UnitXObject(None,None,None,is_none=True), UnitXObject(None,None,None,is_none=True)
	current_scope['x'] = x
	current_scope['y'] = y
	current_scope['dfs'] = DefinedFunction('dfs', [['x', x], ['y', y], ['level', None]], ctx=None)
	Util.dump(current_scope)

	scopes.del_scope()

	return 0


if __name__ == '__main__':
	sys.exit(main())
