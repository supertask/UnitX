#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from unitx_object import UnitXObject
from constants import Constants
from collegue import Collegue

class UnitXObjectCalc(Collegue):
	""" UnitXObject同士の値を計算するクラス．
	"""

	def __init__(self):
		""" scopesを設定して，応答する．
		"""
		pass

	def check_unitx_objects(self, unitx_objs):
		for an_obj in unitx_objs:
			if an_obj.is_none:
				sys.stderr.write("型Error: Noneを演算しようとしている．")
				sys.exit(1)

	def add(self,x,y):
		""" スコープの情報をx,yに注入し，x,yを足して，結果を応答する．
		"""
		self.check_unitx_objects([x,y])
		a_value = (x.get_value() + y.get_value())
		a_unit = x.unit.add(y.unit)
		return UnitXObject(value = a_value, varname=None, unit=a_unit)

	def subtract(self,x,y):
		""" スコープの情報をx,yに注入し，x,yを引いて，結果を応答する．
		"""
		self.check_unitx_objects([x,y])
		a_value = (x.get_value() - y.get_value())
		a_unit = x.unit.subtract(y.unit)
		return UnitXObject(value = a_value, varname=None, unit=a_unit)

	def multiply(self,x,y):
		""" スコープの情報をx,yに注入し，x,yを掛けて，結果を応答する．
		"""
		self.check_unitx_objects([x,y])
		a_value = (x.get_value() * y.get_value())
		a_unit = x.unit.multiply(y.unit)
		return UnitXObject(value = a_value, varname=None, unit=a_unit)

	def divide(self,x,y):
		""" スコープの情報をx,yに注入し，x,yを割って，結果を応答する．
		"""
		self.check_unitx_objects([x,y])
		a_value = (x.get_value() / y.get_value())
		a_unit = x.unit.divide(y.unit)
		return UnitXObject(value = a_value, varname=None, unit=a_unit)

	def increment(self,x):
		""" スコープの情報をx,yに注入し，xをインクリメントして，結果を応答する．
		"""
		self.check_unitx_objects([x])
		return self.add_assign(x, Constants.ONE)

	def decrement(self,x):
		""" スコープの情報をx,yに注入し，xをデクリメントして，結果を応答する．
		"""
		self.check_unitx_objects([x])
		return self.subtract_assign(x, Constants.ONE)


	def assign(self, x, y):
		""" スコープの情報をx,yに注入し，変数xに値yを代入して，結果を応答する．
			スコープに値を入れる唯一の関数．
		"""
		self.check_unitx_objects([x]) # 代入される側のみcheckする．

		x.set_value(y.get_value())
		x.unit = y.unit
		x.unit.remove_ex()
		x.is_none = y.is_none
		self.mediator.get_scopes().regist_unitx_obj(x.varname, x)
		#print self.scopes
		return x


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


	def set_mediator(self, mediator):
		self.mediator = mediator

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
