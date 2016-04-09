#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from unit import Unit
from util import Util
from collegue import Collegue

class UnitXObject(Collegue):
	""" Primary情報（数値，文字列，真偽値，リスト，変数，関数などの情報）を持つクラス．
		手動または自動による単位計算などを計算する関数も束縛する．

		ex: 5, "Tasuku", true, [1,2,3], a_var, 5{MB}, 20{kg->g}, 3{N*m}
	"""

	is_prepared_unit_table = False # start variable

	def __init__(self, value, varname, unit, token=None, is_none=False):
		""" UnitXObjectの初期化
			ここでのvalueとは，数値，文字列，変数名を表す．
		"""
		self.token = token
		self._value = value
		self.varname = varname
		self.is_none = is_none
		self.unit = unit

	def get_value(self, error=True):
		""" UnitXObjectに束縛する数値，文字列，または変数の値を応答する．
			もし，値がなければ変数をスコープから辿り，その値を返す．
			また，呼び出した際にエラー出力したくない場合はerrorをオフにする必要がある．
		"""
		if self._value is None:
			if not self.varname:
				return None
			found_scope = self.mediator.get_scopes().peek().find_scope_of(self.varname)
			if found_scope:
				unitx_obj = found_scope[self.varname]
				if unitx_obj.is_none:
					return None
				else:
					return self._trans_all_unit(unitx_obj.get_value())
			else:
				if error:
					msg = "NameError: name '%s' is not defined." % self.varname
					self.mediator.get_parser().notifyErrorListeners(msg, self.token, Exception(msg))
				else: return None
		else:
			return self._trans_all_unit(self._value)


	def _trans_all_unit(self, value):
		if isinstance(value, list):
			list_values = []
			for v in value:
				v.set_value(self._trans_by_unit(v.get_value()))
				list_values.append(v)
			return list_values
		else:
			return self._trans_by_unit(value)


	def _trans_by_unit(self, value):
		"""
		"""
		if isinstance(value, bool): return value
		if not self.unit or self.unit.is_empty(): return value
		self._check_unit()

		manager = self.mediator.get_unit_manager()
		if not UnitXObject.is_prepared_unit_table: 
			UnitXObject.is_prepared_unit_table = True
			exec(manager.get_prepare_exec(), globals())
			
		trans_value = self._trans_by_original_unit(value)

		if not trans_value:
			if self.unit.numer and self.unit.ex_numer:
				value = value * (manager.get_criterion(self.unit.ex_numer) \
					/ manager.get_criterion(self.unit.numer))

			if self.unit.denom and self.unit.ex_denom:
				value = value * (manager.get_criterion(self.unit.denom) \
					/ manager.get_criterion(self.unit.ex_denom))

			trans_value = float(value)
			if trans_value.is_integer(): trans_value = int(trans_value)

		return trans_value


	def _trans_by_original_unit(self, value):
		"""
		"""
		unit = self.unit
		manager = self.mediator.get_unit_manager()
		unit_id = manager.get_unit_id(self.unit.numer)
		res = eval(manager._unit_evals[unit_id])
		if not isinstance(res, dict):
			return res
		else:
			return None
			


	def _check_unit(self):
		"""
		"""
		manager = self.mediator.get_unit_manager()
		if self.unit.numer and self.unit.ex_numer:
			if manager.get_unit_id(self.unit.numer) != manager.get_unit_id(self.unit.ex_numer):
				sys.stderr.write('Unitが合わない\n')
				sys.exit(1)

		if self.unit.denom and self.unit.ex_denom:
			if manager.get_unit_id(self.unit.denom) != manager.get_unit_id(self.unit.ex_denom):
				sys.stderr.write('Unitが合わない\n')
				sys.exit(1)


	def set_value(self, value):
		self._value = value

	def get_unit(self):
		return self.unit

	def __unicode__(self):
		""" 値と変数を詳細に表示する．
		"""
		return u"<%s: value=%s, varname=%s, is_none=%s unit=%s>" \
			% (self.__class__.__name__, self.get_value(), self.varname, self.is_none, self.unit)

	def __str__(self):
		return unicode(self).encode('utf-8')

	def __repr__(self):
		return self.__str__()

	
	def get_type_string(self, value):
		if isinstance(value, str) or isinstance(value, unicode):
			return 'string'
		elif isinstance(value, list):
			return 'list'
		elif isinstance(value, bool):
			return 'bool'
		elif isinstance(value, int):
			return 'int'
		elif isinstance(value, float):
			return 'float'

	def check_unitx_objects(self, unitx_objs, opp_token):
		"""
		"""
		left_obj,right_obj = unitx_objs

		if type(left_obj.get_value()) is not type(right_obj.get_value()) or \
			left_obj.is_none or right_obj.is_none:
			types = tuple(opp_token.text)
			for an_obj in unitx_objs:
				if an_obj.is_none:
					types += ('NULL',)
				else:
					type_str = self.get_type_string(an_obj.get_value())
					types += (type_str, )

			msg = "TypeError: unsupported operand for %s: '%s' and '%s'" % types
			self.mediator.get_parser().notifyErrorListeners(msg, opp_token, Exception(msg))


	def add(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，x,yを足して，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() + unitx_obj.get_value())
		a_unit = self.unit.add(unitx_obj.unit)
		return UnitXObject(value = a_value, varname=None, unit=a_unit)

	def subtract(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，x,yを引いて，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() - unitx_obj.get_value())
		a_unit = self.unit.subtract(unitx_obj.unit)
		return UnitXObject(value = a_value, varname=None, unit=a_unit)

	def multiply(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，x,yを掛けて，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() * unitx_obj.get_value())
		a_unit = self.unit.multiply(unitx_obj.unit)
		return UnitXObject(value = a_value, varname=None, unit=a_unit)

	def divide(self,x, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，x,yを割って，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() / unitx_obj.get_value())
		a_unit = self.unit.divide(unitx_obj.unit)
		return UnitXObject(value = a_value, varname=None, unit=a_unit)

	def increment(self, opp_token):
		""" スコープの情報をx,yに注入し，xをインクリメントして，結果を応答する．
		"""
		return self.add_assign(UnitXObject(value=1, varname=None, unit=Unit()), opp_token)

	def decrement(self, opp_token):
		""" スコープの情報をx,yに注入し，xをデクリメントして，結果を応答する．
		"""
		return self.subtract_assign(UnitXObject(value=1, varname=None, unit=Unit()), opp_token)


	def assign(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，変数xに値yを代入して，結果を応答する．
			スコープに値を入れる唯一の関数．
		"""
		self.set_value(unitx_obj.get_value())
		self.unit = unitx_obj.unit
		self.unit.remove_ex()
		self.is_none = unitx_obj.is_none
		self.mediator.get_scopes().regist_unitx_obj(self.varname, self)
		return self

	def add_assign(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，x,yを足してxに代入して，結果を応答する．
		"""
		return self.assign(self.add(unitx_obj, opp_token), opp_token)

	def subtract_assign(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，x,yを引いてxに代入して，結果を応答する．
		"""
		return self.assign(self.subtract(unitx_obj, opp_token), opp_token)
		
	def multiply_assign(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，x,yを掛けてxに代入して，結果を応答する．
		"""
		return self.assign(self.multiply(unitx_obj, opp_token), opp_token)

	def divide_assign(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，x,yを割ってxに代入して，結果を応答する．
		"""
		return self.assign(self.divide(unitx_obj, opp_token), opp_token)

	@classmethod
	def set_mediator(self, mediator):
		self.mediator = mediator

def main():
	""" Example: UnitXObjectの変数を保存し，取り出し，確認する．
	"""
	# Prepare part
	from unit_manager import UnitManager
	from scope_list import ScopeList
	from util import Util
	scopes = ScopeList()
	UnitXObject.unit_manager = UnitManager('data/unit_table.dat')
	UnitXObject.scopes = scopes
	scopes.new_scope()
	
	# Regist part
	current_scope = scopes.peek()
	current_scope['x'] = UnitXObject(value=1.5, varname='x', is_none=False, unit=Unit(ex_numer=u'm', numer=u'cm', ex_denom=None, denom=None))
	current_scope['y'] = UnitXObject(value=1500, varname='y', is_none=False, unit=Unit(ex_numer=u'm', numer=u'km', ex_denom=u'時', denom=u'分'))
	scopes.new_scope()
	
	# Find & Show part
	found_scope = scopes.peek().find_scope_of('x')
	Util.dump(scopes)
	#print found_scope['x']
	#print found_scope['y']

	# Clear part
	scopes.del_scope()
	scopes.del_scope()
	return 0

if __name__ == '__main__':
	sys.exit(main())
