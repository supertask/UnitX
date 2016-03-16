#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class UnitXObject:
	""" Primary情報（数値，文字列，真偽値，リスト，変数，関数などの情報）を持つクラス．
		手動または自動による単位計算などを計算する関数も束縛する．

		ex: 5, "Tasuku", true, [1,2,3], is_first, 5{MB}, 20{kg->g}, 3{N*m}
	"""

	""" すべてのスコープを束縛するインスタンス．
	"""
	scopes = None #static変数

	def __init__(self, value, varname, is_none=False):
		""" UnitXObjectの初期化
			ここでのvalueとは，数値，文字列，変数名を表す．
		"""
		self._value = value
		self._varname = varname
		self._is_none = is_none

	def is_none(self):
		""" UnitXObjectがNoneオブジェクトを束縛するかを応答する．
		"""
		return self._is_none

	def get_scopes(self):
		""" すべてのスコープを束縛するインスタンスを応答する．
		"""
		return UnitXObject.scopes


	def get_value(self, error=True):
		""" UnitXObjectに束縛する数値，文字列，または変数の値を応答する．
			また，呼び出した際にエラー出力したくない場合はerrorをオフにする必要がある．
		"""
		if self._value is None:
			varname = self.get_varname(error)
			found_scope = self.get_scopes().peek().find_scope_of(varname)
			if found_scope:
				unitx_obj = found_scope[varname]
				if unitx_obj.is_none(): return None
				else: return unitx_obj.get_value()
			else:
				if error:
					sys.stderr.write("NameError: name '%s' is not defined.\n" % varname)
					raise Exception()
					sys.exit(1)
				else: return None
		else:
			return self._value


	def get_varname(self, error=True):
		""" 変数名を応答する．
			また，呼び出した際にエラー出力したくない場合はerrorをオフにする必要がある．
		"""
		if self._varname: return self._varname
		else:
			if error:
				raise Exception("SystemError: UnitXObjectの値が設定されていない．\n")
				sys.exit(1)
			else: return None
	

	def dump(self):
		""" 値と変数を詳細に表示する．
		"""
		print "_value, _varname, _is_none: %s, %s, %s" % (self.get_value(error=False), self.get_varname(error=False), self.is_none())


def main():
	""" Example: UnitXObjectの変数を保存し，取り出し，確認する．
	"""
	# Prepare part
	from scope_list import ScopeList
	from util import Util
	scopes = ScopeList()
	UnitXObject.scopes = scopes
	scopes.new_scope()
	
	# Regist part
	current_scope = scopes.peek()
	current_scope['x'] = UnitXObject(value=None, varname='x', is_none=True)
	scopes.new_scope()
	
	# Find & Show part
	found_scope = scopes.peek().find_scope_of('x')
	Util.dump(scopes)
	found_scope['x'].dump()

	# Clear part
	scopes.del_scope()
	scopes.del_scope()

	return 0

if __name__ == '__main__':
	sys.exit(main())
