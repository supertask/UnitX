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

	def __init__(self, value, varname, unit, is_none=False):
		""" UnitXObjectの初期化
			ここでのvalueとは，数値，文字列，変数名を表す．
		"""
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
			found_scope = self.get_scopes().peek().find_scope_of(self.varname)
			if found_scope:
				unitx_obj = found_scope[self.varname]
				if unitx_obj.is_none:
					return None
				else:
					return self._trans_all_unit(unitx_obj.get_value())
			else:
				if error:
					sys.stderr.write("NameError: name '%s' is not defined.\n" % self.varname)
					sys.exit(1)
				else: return None
		else:
			return self._trans_all_unit(self._value)


	def _trans_all_unit(self, value):
		if isinstance(value, list):
			list_values = []
			for v in value:
				v.set_value(self._trans_unit(v.get_value()))
				list_values.append(v)
			return list_values
		else:
			return self._trans_unit(value)


	def _trans_unit(self, value):
		"""
		"""
		if isinstance(value, bool): return value
		if isinstance(value, str): return value
		if isinstance(value, unicode): return value
		if not self.unit or self.unit.is_empty(): return value
		self._check_unit(self.unit)

		manager = self.get_unit_manager()
		if self.unit.numer and self.unit.ex_numer:
			value = value * (manager.get_criterion(self.unit.ex_numer) / manager.get_criterion(self.unit.numer))
		if self.unit.denom and self.unit.ex_denom:
			value = value * (manager.get_criterion(self.unit.ex_denom) / manager.get_criterion(self.unit.denom))
		value = float(value)
		if value.is_integer(): value = int(value)

		return value


	def _check_unit(self, unit):
		"""
		"""
		manager = self.get_unit_manager()
		if unit.numer and unit.ex_numer:
			if manager.get_unit_id(unit.numer) != manager.get_unit_id(unit.ex_numer):
				sys.stderr.write('Unitが合わない\n')
				sys.exit(1)
		if unit.denom and unit.ex_denom:
			if manager.get_unit_id(unit.denom) != manager.get_unit_id(unit.ex_denom):
				sys.stderr.write('Unitが合わない\n')
				sys.exit(1)

	def set_value(self, value):
		self._value = value

	def get_scopes(self):
		""" すべてのスコープを束縛するインスタンスを応答する．
		"""
		return UnitXObject.scopes
	
	def get_unit_manager(self):
		return UnitXObject.unit_manager
	
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
