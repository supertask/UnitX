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
		"""現在のスコープ内のメモリを確保する．
		"""
		self.append(Scope(self.peek()))
		return

	def del_scope(self):
		""" 現在のスコープ内のメモリを解放する．
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

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
