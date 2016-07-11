#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from collegue import Collegue
from constants import Constants
from unitx_object import UnitXObject
from unit import Unit

class DefinedFunction(Collegue):
	"""A Class for saving a infomation of defined function.
	
	Attributes:
		name: A string indicating function name.
		args: A list of string indicating function argument.
		ctx: An instance of ParserRuleContext of functionDeclaration RULE.
		_current_scope: A instance of Scope saving an instance of this class.
	"""

	def __init__(self, name, defined_args, ctx=None, func_p=None):
		"""Inits attributes of a DefinedFunction class. """
		self.name = name
		self.defined_args = defined_args
		self.ctx = ctx
		self.func_p = func_p
		#self._current_scope = current_scope


	def call(self, called_args, called_funcobj):
		"""Call a defined function with called arguments.

		Args:
			A list of a argument appointed/called by user.
		Returns:
			A instance of UnitXObject calculated by this function.
		"""

		# variable, default_value: UnitXObject
		args_without_default = []
		for variable, default_value in self.defined_args:
			if not default_value:
				args_without_default.append([variable, None])

		#
		# 引数が足りないエラー
		#
		if len(called_args) < len(args_without_default):
			msg = "TypeError: %s() takes exactly %s arguments (%s given)" \
				% (self.name, len(args_without_default), len(called_args))
			if called_args: 
				last_unitx_obj = called_args[-1]
				self.mediator.get_parser().notifyErrorListeners(msg, last_unitx_obj.token, Exception(msg))
			else: 
				self.mediator.get_parser().notifyErrorListeners(msg, self.ctx.start, Exception(msg))

		#
		# 引数が多すぎるときのエラー
		#
		if len(called_args) > len(self.defined_args):
			msg = "TypeError: %s() takes exactly %s arguments (%s given)" \
				% (self.name, len(self.defined_args), len(called_args))
			last_unitx_obj = called_args[-1]
			self.mediator.get_parser().notifyErrorListeners(msg, last_unitx_obj.token, Exception(msg))


		# TODO(Tasuku): 現在は定義した関数のみ使用可能だが，組み込み関数はまだなので，それを後で追加
		if self.ctx:
			self.define_arguments(called_args)
			self.mediator.visitBlock(self.ctx.block())
			return None
		else:
			# リフレクションで関数を呼び出す
			# Here!!!!
			# called_args: A list of UnitXObject
			#called_args = map(lambda x: x.get_value(), called_args)
			#print 'Debug: ', called_args
			a_value = self.func_p(called_args, called_funcobj)
			if a_value:
				return UnitXObject(value=a_value, varname=None, is_none=False, unit=Unit(), token=called_funcobj.token)
			else:
				return UnitXObject(value=None, varname=None, is_none=True, unit=Unit(), token=called_funcobj.token)


	def define_arguments(self, called_args):
		"""関数の引数の変数たちを定義し，呼び出し時の値たちをそれぞれ代入する"""
		for i in range(len(self.defined_args)):
			variable, default_value = self.defined_args[i]
			if i < len(called_args):
				unitx_obj = called_args[i]
			else:
				if default_value:
					unitx_obj = default_value
				else:
					unitx_obj = UnitXObject(value=None, varname=None, unit=Unit(), token=None, is_none=True)
			variable.assign(unitx_obj, None) #スコープに代入される


		"""Returns a current scope saving this class.
	def get_current_scope(self):

		Returns:
			A instance of Scope saving an instance of this class.
		return self._current_scope
		"""
	

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
