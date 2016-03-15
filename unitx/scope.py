#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" 変数またはインスタンスのスコープを管理するクラス．
"""
class Scope(dict):

	def __init__(self, parent):
		""" 親スコープを初期化して，応答する．
		"""
		self.parent = parent


	def find_scope_of(self, varname):
		""" 現在のスコープ内またはすべての親スコープ内に指定された変数(var_name)があれば，その値を応答する．
		"""
		if varname in self: return self
		else:
			if not self.parent: return None #終了条件
			return self.parent.find_scope_of(varname) #再帰的に探す

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())