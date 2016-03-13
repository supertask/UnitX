#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from unitx_object import UnitXObject

class UnitXObjectCalc:
	""" UnitXObject同士の値を計算するクラス．
	"""

	def __init__(self, scopes):
		""" scopesを設定して，応答する．
		"""
		self.scopes = scopes #scopesの参照をself.scopesに渡す．またscopesは読み取りのみでなければならない．

	def get_scopes(self):
		""" スコープの情報を応答する．
			また，self.scopesは書き込むと参照渡しが無効になるため，読み取りのみでなければならない．
		"""
		return self.scopes

	def inject_scopes_to(self, unitx_objs):
		""" スコープの情報を引数で与えられたUnitXObjectたちに注入する． 
		"""
		for an_obj in unitx_objs: an_obj.set_scopes(self.scopes)

	def add(self,x,y):
		""" x,yを足して，応答する．
		"""
		self.inject_scopes_to([x,y])
		a_value = (x.get_value() + y.get_value())
		return UnitXObject(a_value)

	def subtract(self,x,y):
		""" x,yを引いて，応答する．
		"""
		self.inject_scopes_to([x,y])
		a_value = (x.get_value() - y.get_value())
		return UnitXObject(a_value)

	def multiply(self,x,y):
		""" x,yを掛けて，応答する．
		"""
		self.inject_scopes_to([x,y])
		a_value = (x.get_value() * y.get_value())
		return UnitXObject(a_value)

	def divide(self,x,y):
		""" x,yを割って，応答する．
		"""
		self.inject_scopes_to([x,y])
		a_value = (x.get_value() / y.get_value())
		return UnitXObject(a_value)

	def increment(self,x):
		""" xをインクリメントして，応答する．
		"""
		self.inject_scopes_to([x])
		return UnitXObject(x.get_value()+1)

	def decrement(self,x):
		""" xをデクリメントして，応答する．
		"""
		self.inject_scopes_to([x])
		return UnitXObject(x.get_value()-1)

	def assign(self, x, y):
		""" 変数xに値yを代入する．
		"""
		varname = x.get_varname()
		current_scope = self.get_scopes()[-1]
		found_scope = current_scope.find_scope_of(varname)
		if found_scope: found_scope[varname] = y.get_value() #Already created variable.
		else: current_scope[varname] = y.get_value() #Create variable.
		return y.get_value()

	def add_assign(self, x, y):
		""" x,yを足してxに代入して，応答する．
		"""
		return self.assign(x, self.add(x,y))

	def subtract_assign(self, x, y):
		""" x,yを引いてxに代入して，応答する．
		"""
		return self.assign(x, self.subtract(x,y))
		
	def multiply_assign(self, x, y):
		""" x,yを掛けてxに代入して，応答する．
		"""
		return self.assign(x, self.multiply(x,y))

	def divide_assign(self, x, y):
		""" x,yを割ってxに代入して，応答する．
		"""
		return self.assign(x, self.divide(x,y))


def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
