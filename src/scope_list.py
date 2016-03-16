#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scope import Scope

""" 変数またはインスタンスのスコープたちを管理するクラス．
"""
class ScopeList(list):

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
			pythonのリストにはpeekメソッドがないため定義．

			Looks at the object at the top of this stack without removing it from the list(stack).
			I defined because a list of python don't have peek method.
		"""
		return self[-1]

	def regist_unitx_obj(self, varname, unitx_obj):
		""" スコープに，変数名とその値（UnitXObject）を登録して，応答する．

			varname -- A key registing in a scope
			unitx_obj -- A value registing in a scope
		"""
		current_scope = self.peek()
		found_scope = current_scope.find_scope_of(varname)
		if found_scope: found_scope[varname] = unitx_obj #Already created variable.
		else: current_scope[varname] = unitx_obj #Create variable in the scope.
		return

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
