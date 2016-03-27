#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
from fractions import Fraction

class UnitManager(object):
	""" 単位の情報を読み取り保存するクラス．
	"""

	def __init__(self, filename):
		""" UnitManagerの初期化
		"""
		self.filename = filename
		self.unit_dict = {}
		self._unit_id_dict = {}
		self._unit_evals = []
		self._is_updated = []
		self._read()


	def _read(self):
		"""
		"""
		with codecs.open(self.filename, 'r', encoding='utf-8') as rf:
			unit_id = 0
			line = rf.readline()
			while line:
				if line.rstrip() == '--':
					key_line = rf.readline().rstrip()
					unit_eval = rf.readline().rstrip()
					tokens = key_line.split()
					for a_token in tokens:
						self._unit_id_dict[a_token] = unit_id
					self._unit_evals.append(unit_eval)
					self._is_updated.append(False)
					unit_id += 1
				line = rf.readline()


	def _update_dict(self, unit_str):
		"""
		"""
		unit_id = self.get_unit_id(unit_str)
		if self._is_updated[unit_id]:
			return
		adding_dict = eval(self._unit_evals[unit_id])
		self.unit_dict.update(adding_dict)
		self._is_updated[unit_id] = True
		return
		

	def get_criterion(self, unit_str):
		"""
		"""
		self._update_dict(unit_str)
		return self.unit_dict[unit_str]


	def get_unit_id(self, unit_str):
		"""
		"""
		from util import Util
		if unit_str in self._unit_id_dict:
			return self._unit_id_dict[unit_str]
		else:
			sys.stderr.write('Unitががありません\n')
			sys.exit(1)


def main():
	manager = UnitManager('unit_table.txt')
	minute = manager.get_criterion(u'分')
	hour = manager.get_criterion(u'時')
	value = 120 * (hour / minute)
	
	from util import Util
	Util.dump(manager.unit_dict)
	print u'kind of unit:', manager.get_unit_id(u'分')
	print value

	return 0


if __name__ == '__main__':
	sys.exit(main())
