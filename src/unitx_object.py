#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from unit import Unit
from util import Util
from collegue import Collegue
from constants import Constants

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

			found_scope = UnitXObject.scopes.peek().find_scope_of(self.varname)
			if found_scope:
				unitx_obj = found_scope[self.varname]
				if unitx_obj.is_none:
					return None
				else:
					return self.__trans_all_unit(unitx_obj.get_value())
			else:
				if error:
					msg = Constants.NAME_ERR % self.varname
					self.mediator.get_parser().notifyErrorListeners(msg, self.token, Exception(msg))
				else: return None
		else:
			return self.__trans_all_unit(self._value)

	def get_unit_value(self):
		return "%s%s" % (self.get_value(), self.unit.formal_str())


	def __trans_all_unit(self, value):
		if isinstance(value, list):
			list_values = []
			for v in value:
				v.set_value(self.__trans_a_unit(v.get_value()))
				list_values.append(v)
			return list_values
		else:
			return self.__trans_a_unit(value)


	def __trans_a_unit(self, value):
		"""
		"""
		if isinstance(value, bool): return value
		if not self.unit or self.unit.is_empty(): return value
		self._check_unit()

		if not UnitXObject.is_prepared_unit_table: 
			UnitXObject.is_prepared_unit_table = True
			exec(UnitXObject.manager.get_prepare_exec(), globals())
			
		trans_value = self._trans_by_original_unit(value)
		if trans_value: return trans_value
		if isinstance(value, unicode): return value

		if self.unit.numer and self.unit.ex_numer:
			value = value * (UnitXObject.manager.get_criterion(self.unit.ex_numer, self.unit) / UnitXObject.manager.get_criterion(self.unit.numer, self.unit))
		if self.unit.denom and self.unit.ex_denom:
			value = value * (UnitXObject.manager.get_criterion(self.unit.denom, self.unit) / UnitXObject.manager.get_criterion(self.unit.ex_denom, self.unit))

		trans_value = float(value)
		if trans_value.is_integer(): trans_value = int(trans_value)

		return trans_value


	def _trans_by_original_unit(self, value):
		"""
		"""
		unit = self.unit # For eval!
		unit_id = UnitXObject.manager.get_unit_id(self.unit.numer, self.unit)
		res = eval(UnitXObject.manager._unit_evals[unit_id])
		if not isinstance(res, dict):
			return res
		else:
			return None
			


	def _check_unit(self):
		"""

		example:
		<ex_numer> -> <numer>
		<ex_denom> -> <denom>
		"""
		if self.unit.numer and self.unit.ex_numer:
			if UnitXObject.manager.get_unit_id(self.unit.numer, self.unit) != UnitXObject.manager.get_unit_id(self.unit.ex_numer, self.unit):
				msg = Constants.TYPE_ERR % (self.unit.ex_numer, self.unit.numer)
				self.mediator.get_parser().notifyErrorListeners(msg, self.unit.token, Exception(msg))

		if self.unit.denom and self.unit.ex_denom:
			if UnitXObject.manager.get_unit_id(self.unit.denom, self.unit) != UnitXObject.manager.get_unit_id(self.unit.ex_denom, self.unit):
				msg = Constants.TYPE_ERR % (self.unit.ex_denom, self.unit.denom)
				self.mediator.get_parser().notifyErrorListeners(msg, self.unit.token, Exception(msg))


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
		""" 左辺と右辺のチェックし，エラーハンドリングを行う．
		"""
		left_obj,right_obj = unitx_objs
		lvalue, rvalue = left_obj.get_value(), right_obj.get_value()
		if isinstance(lvalue, int) and isinstance(rvalue, int): return
		if isinstance(lvalue, int) and isinstance(rvalue, float): return
		if isinstance(lvalue, float) and isinstance(rvalue, int): return
		if isinstance(lvalue, float) and isinstance(rvalue, float): return

		if type(left_obj.get_value()) is not type(right_obj.get_value()) or \
			left_obj.is_none or right_obj.is_none:
			types = tuple()
			for an_obj in unitx_objs:
				if an_obj.is_none:
					types += ('NULL',)
				else:
					type_str = self.get_type_string(an_obj.get_value())
					types += (type_str, )

			msg = Constants.TYPE_ERR_UNSUPPORTED_VALUE % ((opp_token.text,) + types)
			self.mediator.get_parser().notifyErrorListeners(msg, opp_token, Exception(msg))


	def add(self, unitx_obj, opp_token):
		""" 左辺と右辺を足した後，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() + unitx_obj.get_value())
		a_unit = self.unit.add(unitx_obj.unit, opp_token)

		return UnitXObject(value = a_value, varname=None, unit=a_unit)


	def subtract(self, unitx_obj, opp_token):
		""" 左辺から右辺を引いた後，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() - unitx_obj.get_value())
		a_unit = self.unit.subtract(unitx_obj.unit, opp_token)

		return UnitXObject(value = a_value, varname=None, unit=a_unit)


	def multiply(self, unitx_obj, opp_token):
		""" 左辺と右辺を掛けた後，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() * unitx_obj.get_value())
		a_unit = self.unit.multiply(unitx_obj.unit, opp_token)

		return UnitXObject(value = a_value, varname=None, unit=a_unit)


	def divide(self, unitx_obj, opp_token):
		""" 左辺から右辺を割った後，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() / unitx_obj.get_value())
		a_unit = self.unit.divide(unitx_obj.unit, opp_token)

		return UnitXObject(value = a_value, varname=None, unit=a_unit)


	def modulo(self, unitx_obj, opp_token):
		""" 左辺から右辺をモジュロ演算した後，結果を応答する．
		"""
		self.check_unitx_objects([self, unitx_obj], opp_token)
		a_value = (self.get_value() % unitx_obj.get_value())
		a_unit = self.unit.modulo(unitx_obj.unit, opp_token)

		return UnitXObject(value = a_value, varname=None, unit=a_unit)


	def increment(self, opp_token):
		""" 自身の値をインクリメントして，結果を応答する．
		"""
		return self.add_assign(UnitXObject(value=1, varname=None, unit=Unit()), opp_token)

	def decrement(self, opp_token):
		""" 自身の値をデクリメントして，結果を応答する．
		"""
		return self.subtract_assign(UnitXObject(value=1, varname=None, unit=Unit()), opp_token)

	
	#TODO(Tasuku): opp_tokenを消す
	def assign(self, unitx_obj, opp_token):
		""" スコープの情報をx,yに注入し，変数xに値yを代入して，結果を応答する．
			スコープに値を入れる唯一の関数．
			ただし，tokenは代入しない．
		"""
		self.set_value(unitx_obj.get_value())
		self.unit = unitx_obj.unit
		self.unit.remove_ex()
		self.is_none = unitx_obj.is_none
		UnitXObject.scopes.regist_unitx_obj(self.varname, self)
		return self

	def add_assign(self, unitx_obj, opp_token):
		""" 左辺と右辺を足した後，左辺に代入して，結果を応答する．
		"""
		return self.assign(self.add(unitx_obj, opp_token), opp_token)

	def subtract_assign(self, unitx_obj, opp_token):
		""" 左辺から右辺を引いた後，左辺に代入して，結果を応答する．
		"""
		return self.assign(self.subtract(unitx_obj, opp_token), opp_token)
		
	def multiply_assign(self, unitx_obj, opp_token):
		""" 左辺と右辺を掛けた後，左辺に代入して，結果を応答する．
		"""
		return self.assign(self.multiply(unitx_obj, opp_token), opp_token)

	def divide_assign(self, unitx_obj, opp_token):
		""" 左辺から右辺を割った後，左辺に代入して，結果を応答する．
		"""
		return self.assign(self.divide(unitx_obj, opp_token), opp_token)

	def modulo_assign(self, unitx_obj, opp_token):
		""" 左辺から右辺をモジュロ演算した後，左辺に代入して，結果を応答する．
		"""
		return self.assign(self.modulo(unitx_obj, opp_token), opp_token)

	def equals(self, unitx_obj):
		return self == unitx_obj

	def __eq__(self, unitx_obj):
		"""
		"""
		value_eq = (self.get_value() == unitx_obj.get_value())
		unit_eq = self.unit.equals(unitx_obj.unit)
		return UnitXObject(value = (value_eq and unit_eq), varname=None, unit=Unit())
	
	@classmethod
	def set_mediator(self, mediator):
		self.mediator = mediator


def main():
	""" Example: UnitXObjectの変数を保存し，取り出し，確認する．
	"""
	from simulator import Simulator
	s = Simulator()
	UnitXObject.manager = s.get_manager()
	UnitXObject.scopes = s.get_scopes()
	
	# Regist part
	crr_scope = s.get_scopes().peek()
	crr_scope['x'] = UnitXObject(value=1.5, varname='x', is_none=False, unit=Unit(ex_numer=u'm', numer=u'cm', ex_denom=None, denom=None))
	crr_scope['y'] = UnitXObject(value=1500, varname='y', is_none=False, unit=Unit(ex_numer=u'm', numer=u'km', ex_denom=u'時', denom=u'分'))
	s.get_scopes().new_scope()
	
	# Find & Show part
	found_scope = s.get_scopes().peek().find_scope_of('x')
	Util.dump(s.get_scopes())

	# Checking equals()
	tmp_obj = UnitXObject(value=1.5, varname='x', is_none=False, unit=Unit(ex_numer=None, numer=u'cm', ex_denom=None, denom=None))
	print tmp_obj
	print crr_scope['x'] == tmp_obj

	# Clear part
	s.get_scopes().del_scope()
	s.get_scopes().del_scope()
	return Constants.EXIT_SUCCESS

if __name__ == '__main__':
	sys.exit(main())
