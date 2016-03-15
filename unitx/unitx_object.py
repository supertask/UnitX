#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class UnitXObject:
	""" 数値と単位を持つクラス．
		手動または自動による単位計算などを計算する関数も束縛する．
		ex: 5{MB}, 20{kg->g}, 3{N*m}
	"""

	""" すべてのスコープを束縛するインスタンス．
	"""
	scopes = None #static変数

	def __init__(self, value, varname):
		""" UnitXObjectの初期化
			ここでのvalueとは，数値，文字列，変数名を表す．
		"""
		self.value = value
		self.varname = varname

	def get_scopes(self):
		""" すべてのスコープを束縛するインスタンスを応答する．
		"""
		return UnitXObject.scopes


	def get_value(self, error=True):
		""" UnitXObjectに束縛する数値，文字列，または変数の値を応答する．
			また，呼び出した際にエラー出力したくない場合はerrorをオフにする必要がある．
		"""
		if self.value: return self.value
		else:
			current_scope = self.get_scopes()[-1]
			found_scope = current_scope.find_scope_of(self.get_varname())
			if found_scope:
				return found_scope[self.varname].get_value()
			else:
				if error:
					sys.stderr.write("""NameError: name '%s' is not defined.\n""" % self.get_varname())
					sys.exit(1)
				else: return None


	def get_varname(self, error=True):
		""" 変数名を応答する．
			また，呼び出した際にエラー出力したくない場合はerrorをオフにする必要がある．
		"""
		if self.varname: return self.varname
		else:
			if error:
				raise Exception("SystemError: UnitXObjectの値が設定されていない．\n")
				sys.exit(1)
			else: return None
	
	def dump_both(self):
		""" 値と変数を詳細に表示する．
		"""
		print "value, varname: %s, %s" % (self.get_value(error=False), self.get_varname(error=False))


def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
