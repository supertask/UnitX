#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from unit import Unit

class UnitXObject:
	""" Primary情報（数値，文字列，真偽値，リスト，変数，関数などの情報）を持つクラス．
		手動または自動による単位計算などを計算する関数も束縛する．

		ex: 5, "Tasuku", true, [1,2,3], is_first, 5{MB}, 20{kg->g}, 3{N*m}
	"""

	""" すべてのスコープを束縛するインスタンス．
		Also, this is a static variable.
	"""
	scopes = None

	""" Unitの管理者を束縛するインスタンス．
		Also, this is a static variable.
	"""
	unit_manager = None 

	def __init__(self, value, varname, is_none=False, unit=None):
		""" UnitXObjectの初期化
			ここでのvalueとは，数値，文字列，変数名を表す．
		"""
		self._value = value
		self._varname = varname
		self._is_none = is_none
		self._unit = unit

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
				else:
					return self._trans_unit(unitx_obj.get_value())
			else:
				if error:
					sys.stderr.write("NameError: name '%s' is not defined.\n" % varname)
					#raise Exception()
					sys.exit(1)
				else: return None
		else:
			return self._trans_unit(self._value)


	def _trans_unit(self, value):
		"""
		"""
		unit, ex_unit = self.get_unit(), self.get_ex_unit()
		if ex_unit: self._check_unit(unit, ex_unit)

		if isinstance(value, bool):
			pass #エラー
		elif isinstance(value, str):
			pass #エラー

		# TODO(Tasuku): ここからエラー
		if unit.numer and unit.ex_numer:
			value = value * (self.get_unit_manager().get_criterion(unit.ex_numer) / self.get_unit_manager().get_criterion(unit.numer))
		if unit.denom and unit.ex_denom:
			value = value * (self.get_unit_manager().get_criterion(unit.ex_denom) / self.get_unit_manager().get_criterion(unit.denom))
		value = float(value)
		if value.is_integer(): value = int(value)
		return value


	def _check_unit(self, unit, ex_unit):
		"""
		"""
		if not unit.ex_numer: unit.ex_numer = ex_unit.numer
		if not unit.ex_denom: unit.ex_denom = ex_unit.denom
		if unit.numer and unit.ex_numer:
			if self.get_unit_manager().get_unit_id(unit.numer) != self.get_unit_manager().get_unit_id(unit.ex_numer):
				sys.stderr.write('Unitが合わない\n')
				sys.exit(1)
		if unit.denom and unit.ex_denom:
			if self.get_unit_manager().get_unit_id(unit.denom) != self.get_unit_manager().get_unit_id(unit.ex_denom):
				sys.stderr.write('Unitが合わない\n')
				sys.exit(1)


	def get_ex_unit(self):
		"""
		"""
		varname = self.get_varname()
		found_scope = self.get_scopes().peek().find_scope_of(varname)
		if found_scope:
			unitx_obj = found_scope[varname]
			return unitx_obj.get_unit()
		else:
			return None


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

	def is_none(self):
		""" UnitXObjectがNoneオブジェクトを束縛するかを応答する．
		"""
		return self._is_none

	def get_scopes(self):
		""" すべてのスコープを束縛するインスタンスを応答する．
		"""
		return UnitXObject.scopes
	
	def get_unit_manager(self):
		return UnitXObject.unit_manager
	
	def get_unit(self):
		return self._unit
	

	def __unicode__(self):
		""" 値と変数を詳細に表示する．
		"""
		return u"<%s: value=%s, varname=%s, is_none=%s unit=%s>" \
			% (self.__class__.__name__, self.get_value(), self.get_varname(), self.is_none(), self.get_unit())

	def __str__(self):
		return unicode(self).encode('utf-8')

	def __repr__(self):
		return self.__str__()


def main():
	""" Example: UnitXObjectの変数を保存し，取り出し，確認する．
	"""
	# Prepare part
	from unit_manager import UnitManager
	from scope_list import ScopeList
	from util import Util
	scopes = ScopeList()
	UnitXObject.unit_manager = UnitManager('unit_table.txt')
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
