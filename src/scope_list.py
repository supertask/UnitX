#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scope import Scope
from collegue import Collegue

""" 変数またはインスタンスのスコープたちを管理するクラス．
"""
class ScopeList(list, Collegue):

	def __init__(self):
		""" スコープのルートを初期化して，応答する．
		"""
		self.append(Scope(parent=None))
		self._current_scope = self.peek()

	def new_scope(self):
		""" 現在のスコープ内のメモリを確保して，応答する．
		"""
		self.append(Scope(self.peek()))
		self.set_current_scope()
		return

	def del_scope(self):
		""" 現在のスコープ内のメモリを解放して，応答する．
		"""
		self.pop()
		self.set_current_scope()
		return

	def peek(self):
		""" スタックの先頭にあるオブジェクトを取り出し応答する．ただし，このときオブジェクトはスタックから削除されない．
			pythonのリストにはpeekメソッドがないため定義．

			Looks at the object at the top of this stack without removing it from the list(stack).
			I defined because a list of python don't have peek method.
		"""
		return self[-1]
	
	def set_current_scope(self, current_scope=None):
		"""
		"""
		if current_scope is None: current_scope = self.peek()
		self._current_scope = current_scope

	def get_current_scope(self):
		"""
		"""
		return self._current_scope

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
		self.mediator = mediator

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
