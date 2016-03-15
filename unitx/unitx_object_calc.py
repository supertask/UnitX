#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from unitx_object import UnitXObject
from constants import Constants

class UnitXObjectCalc:
	""" UnitXObject同士の値を計算するクラス．
	"""

	def __init__(self, scopes):
		""" scopesを設定して，応答する．
		"""
		self.scopes = scopes #scopesの参照をself.scopesに渡す．またscopesは読み取りのみでなければならない．

	def get_scopes(self):
		""" スコープの情報を応答する．
			また，self.const.scopesは書き込むと参照渡しが無効になるため，読み取りのみでなければならない．
		"""
		return self.scopes

	def add(self,x,y):
		""" スコープの情報をx,yに注入し，x,yを足して，結果を応答する．
		"""
		a_value = (x.get_value() + y.get_value())
		return UnitXObject(value = a_value, varname=None)

	def subtract(self,x,y):
		""" スコープの情報をx,yに注入し，x,yを引いて，結果を応答する．
		"""
		a_value = (x.get_value() - y.get_value())
		return UnitXObject(value = a_value, varname=None)

	def multiply(self,x,y):
		""" スコープの情報をx,yに注入し，x,yを掛けて，結果を応答する．
		"""
		a_value = (x.get_value() * y.get_value())
		return UnitXObject(value = a_value, varname=None)

	def divide(self,x,y):
		""" スコープの情報をx,yに注入し，x,yを割って，結果を応答する．
		"""
		a_value = (x.get_value() / y.get_value())
		return UnitXObject(value = a_value, varname=None)

	def increment(self,x):
		""" スコープの情報をx,yに注入し，xをインクリメントして，結果を応答する．
		"""
		return self.add_assign(x, Constants.ONE)

	def decrement(self,x):
		""" スコープの情報をx,yに注入し，xをデクリメントして，結果を応答する．
		"""
		return self.subtract_assign(x, Constants.ONE)

	## 
	# スコープに値を入れる唯一の関数
	##
	def assign(self, x, y):
		""" スコープの情報をx,yに注入し，変数xに値yを代入して，結果を応答する．
		"""
		varname = x.get_varname(error=True) #変数名が登録されていなければ，error処理をする
		current_scope = self.get_scopes()[-1]
		found_scope = current_scope.find_scope_of(varname)

		an_obj = UnitXObject(value = y.get_value(), varname=varname)
		if found_scope:
			found_scope[varname] = an_obj #Already created variable.
		else:
			current_scope[varname] = an_obj #Create variable.
		return an_obj

	def add_assign(self, x, y):
		""" スコープの情報をx,yに注入し，x,yを足してxに代入して，結果を応答する．
		"""
		return self.assign(x, self.add(x,y))

	def subtract_assign(self, x, y):
		""" スコープの情報をx,yに注入し，x,yを引いてxに代入して，結果を応答する．
		"""
		return self.assign(x, self.subtract(x,y))
		
	def multiply_assign(self, x, y):
		""" スコープの情報をx,yに注入し，x,yを掛けてxに代入して，結果を応答する．
		"""
		return self.assign(x, self.multiply(x,y))

	def divide_assign(self, x, y):
		""" スコープの情報をx,yに注入し，x,yを割ってxに代入して，結果を応答する．
		"""
		return self.assign(x, self.divide(x,y))


def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
