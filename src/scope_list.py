#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from scope import Scope
from collegue import Collegue
from constants import Constants
from util import Util

class ScopeList(list, Collegue):
	"""A class managing instances of a Scope class.
	
	Actually, This is implemented by a list.
	But it has some functions because this lang needs to create and delete a scope.
	"""

	def __init__(self):
		"""Pushes an empty scope into the top of this ScopeList."""
		self.append(Scope(parent=None))

	def new_scope(self):
		"""Pushes an empty scope into the top of this ScopeList
		
		To put it simply, it means "create new current scope".
		"""
		self.append(Scope(self.peek()))
		return

	def del_scope(self):
		"""Deletes a scope which is already used from the top of this ScopeList

		To put it simply, it means "delete new current scope".
		"""
		self.pop()
		return


	def peek(self):
		"""Returns a scope which is located to the top of this stack without removing it.

		I defined this function because a list of Python doesn't 
		have peek() method. I think a list of Python should have 
		the pretty much function.

		Returns:
			self[-1]: An instance of a scope that is used currently.
		"""
		return self[-1]


	def regist_unitx_obj(self, varname, unitx_obj):
		"""Registers an instance of a variable name and a unitx object into a current scope.

		Args:
			varname: A string of variable registing in a scope
			unitx_obj: An instance of UnitXObject registing in a scope
		"""
		current_scope = self.peek()
		current_scope[varname] = unitx_obj
		return


	def set_mediator(self, mediator):
		"""Sets a mediator for Mediator pattern of GoF.
		
		Args:
			mediator: An instance of a EvalVisitor class inherited Mediator class.
		"""
		self.mediator = mediator

def main():
	"""Run an example for a ScopeList class."""
	from unitx_object import UnitXObject
	from unit import Unit

	scopes = ScopeList()
	scopes.new_scope()
	scopes.peek()['x'] = UnitXObject(value=2, varname='x', unit=Unit())
	scopes.new_scope()
	scopes.peek()['y'] = UnitXObject(value=3, varname='y', unit=Unit())

	Util.dump(scopes)
	scopes.del_scope()
	Util.dump(scopes)
	scopes.del_scope()
	Util.dump(scopes)

	return Constants.EXIT_SUCCESS

if __name__ == '__main__':
	sys.exit(main())
