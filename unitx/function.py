#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from constants import Constants
from collegue import Collegue
from unitx_object import UnitXObject
from unit import Unit
from util import Util

class Function(Collegue):
	"""A Class for saving a infomation of defined function.
	
	Attributes:
		name: A string indicating function name.
		args: A list of string indicating function argument.
		ctx: An instance of ParserRuleContext of functionDeclaration RULE.
		_current_scope: A instance of Scope saving an instance of this class.
	"""

	def __init__(self, name, defined_args, ctx=None, func_p=None, code=None):
		"""Inits attributes of a Function class. """
		self.name = name
		self.defined_args = defined_args
		self.ctx = ctx
		self.func_p = func_p
		self.func_obj = None
		self.called_func = None
		self.code = code


	def call(self, args, func_obj, called_func):
		"""Call a defined function with called arguments.

		Args:
			A list of a argument appointed/called by user.
		Returns:
			A instance of UnitXObject calculated by this function.
		"""
		self.check_arguments(args, func_obj, called_func)
		return None


	def check_arguments(self, args, func_obj, called_func):
		"""
		"""
		self.func_obj = func_obj
		self.called_func = called_func

		# variable, default_value: UnitXObject
		args_without_default = []
		for variable, default_value in self.defined_args:
			if not default_value:
				args_without_default.append([variable, None])

		#
		# 引数が足りないエラー
		#
		if len(args) < len(args_without_default):
			msg = Constants.TYPE_ERR_ARGS % (self.name, len(args_without_default), len(args))
			if args: 
				last_unitx_obj = args[-1]
				self.mediator.get_parser().notifyErrorListeners(msg, last_unitx_obj.token, Exception(msg))
			else: 
				self.mediator.get_parser().notifyErrorListeners(msg, self.ctx.start, Exception(msg))

		#
		# 引数が多すぎるときのエラー
		#
		if len(args) > len(self.defined_args):
			msg = Constants.TYPE_ERR_ARGS % (self.name, len(self.defined_args), len(args))
			last_unitx_obj = args[-1]
			self.mediator.get_parser().notifyErrorListeners(msg, last_unitx_obj.token, Exception(msg))
		return


	def __unicode__(self):
		"""Returns a string of attributes.

		Returns:
			A string of infomations of attributes.
		"""
		res = "<%s: %s(%s) ctx=%s func_p=%s>" % (self.__class__.__name__, self.name, self.defined_args, self.ctx, self.func_p)
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



class DefinedFunction(Function):
	def __init__(self, name, defined_args, ctx, code):
		super(DefinedFunction, self).__init__(name, defined_args, ctx=ctx, code=code)
	
	def call(self, args, func_obj, called_func):
		super(DefinedFunction, self).call(args, func_obj, called_func)
		self.define_arguments(args)
		self.mediator.visitBlock(self.ctx.block())
		return self.mediator.return_value

	def define_arguments(self, args):
		"""関数の引数の変数たちを定義し，呼び出し時の値たちをそれぞれ代入する"""
		for i in range(len(self.defined_args)):
			variable, default_value = self.defined_args[i]
			if i < len(args):
				unitx_obj = args[i]
			else:
				if default_value:
					unitx_obj = default_value
				else:
					unitx_obj = UnitXObject(value=None, varname=None, unit=Unit(), token=None, is_none=True)
			variable.assign(unitx_obj, None) #スコープに代入される



class BuiltInFunction(Function):
	def __init__(self, name, defined_args, func_p):
		super(BuiltInFunction, self).__init__(name, defined_args, func_p=func_p)
	
	def call(self, args, func_obj, called_func):
		super(BuiltInFunction, self).call(args, func_obj, called_func)
		a_value = self.func_p(args, func_obj)
		if a_value:
			return UnitXObject(value=a_value, varname=None, is_none=False, unit=Unit(), token=func_obj.token)
		else:
			return UnitXObject(value=None, varname=None, is_none=True, unit=Unit(), token=func_obj.token)


def main():
	"""Run an example for a Function class.

	Advice:
		A value of 'ctx' should get from an argument of visitFunctionDeclaration(ctx).
	"""
	from simulator import Simulator
	s = Simulator()

	# Define variables
	current_scope = s.get_scopes().peek()
	x, y = UnitXObject(None,None,None,is_none=True), UnitXObject(None,None,None,is_none=True)
	current_scope['x'] = x
	current_scope['y'] = y
	current_scope['dfs'] = DefinedFunction('dfs', [['x', x], ['y', y], ['level', None]], ctx=None, code=None)

	# Output
	from util import Util
	Util.dump(current_scope)
	s.get_scopes().del_scope()

	return Constants.EXIT_SUCCESS

if __name__ == '__main__':
	sys.exit(main())
