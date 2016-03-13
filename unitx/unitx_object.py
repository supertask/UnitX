#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class UnitXObject:
	""" 数値と単位を持つクラス．
		手動または自動による単位計算などを計算する関数も束縛する．
		ex: 5{MB}, 20{kg->g}, 3{N*m}
	"""

	def __init__(self, value_or_varnmae, is_identifier=False):
		""" UnitXObjectの初期化
			ここでのvalueとは，数値，文字列，変数名を表す．
		"""
		self.is_identifier = is_identifier
		if self.is_identifier:
			self.varname = value_or_varnmae
		else:
			self.value = value_or_varnmae

	def set_scopes(self, scopes):
		""" スコープインスタンスを束縛する．
		"""
		self.scopes = scopes

	def get_value(self):
		""" UnitXObjectに束縛する数値，文字列，または変数の値を応答する．
		"""
		if self.is_identifier:
			current_scope = self.scopes[-1]
			found_scope = current_scope.find_scope_of(self.get_varname())
			if found_scope:
				return found_scope[self.varname]
			else:
				sys.stderr.write("""NameError: name '%s' is not defined.\n""" % self.get_varname())
				sys.exit(1)
		else: return self.value
	
	def get_varname(self):
		""" 変数名を応答する．
		"""
		if self.is_identifier: return self.varname
		else:
			sys.stderr.write("""SyntaxError: can't assign to literal.\n""")
			sys.exit(1)

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
