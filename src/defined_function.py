#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

class DefinedFunction(object):
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
	
	def dump(self):
		""" Outputs attributes bound by this class.
		"""
		sys.stdout.write("DefinedFunction: name=%s, args=%s ctx=%s\n" % (self.name, self.args, self.ctx))
		return

def main():
	""" A example code.

		A value of 'func_name' should get by using visitFormalParameters(ctx).
		Also, a value of 'ctx' should get from argument of visitFunctionDeclaration(ctx).
	"""
	from unitx_object import UnitXObject
	x, y = UnitXObject(None,None,is_none=True), UnitXObject(None,None,is_none=True)
	func_name = 'dfs'
	func_args = [['x', x], ['y', y], ['level', None]]
	ctx = None
	def_func = DefinedFunction(func_name, func_args, ctx)
	def_func.dump()

	return 0


if __name__ == '__main__':
	sys.exit(main())
