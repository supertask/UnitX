#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scope import Scope
from collegue import Collegue
from constants import Constants

class ScopeList(list, Collegue):
	"""変数またはインスタンスのスコープたちを管理するクラス．

	"""

	def __init__(self):
		""" スコープのルートを初期化して，応答する．
		"""
		self.append(Scope(parent=None))


	def new_scope(self):
		""" 現在のスコープ内のメモリを確保して，応答する．
		"""
		self.append(Scope(self.peek()))
		return


	def del_scope(self):
		""" 現在のスコープ内のメモリを解放して，応答する．
		"""
		self.pop()
		return


	def peek(self):
		""" スタックの先頭にあるオブジェクトを取り出し応答する．ただし，このときオブジェクトはスタックから削除されない．

			Looks at the object at the top of this stack without removing it 
			from the list(stack).

			I defined this function because a list of Python doesn't 
			have peek() method. I think a list of Python should have 
			the pretty much function.

			Returns:
				
		"""
		return self[-1]

	
	def get_current_scope(self):
		"""
		"""
		return self.peek()


	def regist_unitx_obj(self, varname, unitx_obj):
		""" スコープに，変数名とその値（UnitXObject）を登録して，応答する．

			varname: A string of variable registing in a scope
			unitx_obj: An instance of UnitXObject registing in a scope
		"""
		current_scope = self.get_current_scope()
		found_scope = current_scope.find_scope_of(varname)
		if found_scope: found_scope[varname] = unitx_obj #Already created variable.
		else: current_scope[varname] = unitx_obj #Create variable in the scope.
		return


	def set_mediator(self, mediator):
		"""Sets a mediator for Mediator pattern of GoF.
		
		Args:
			mediator: An instance of a EvalVisitor class inherited Mediator class.
		"""
		self.mediator = mediator


def main():
	return Constants.EXIT_SUCCESS

if __name__ == '__main__':
	sys.exit(main())
