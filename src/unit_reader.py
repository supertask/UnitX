#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
from fractions import Fraction

class UnitReader(object):
	""" 単位の情報を読み取り保存するクラス．
	"""

	def __init__(self, filename):
		""" UnitReaderの初期化
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
		if unit_str in self._unit_id_dict:
			return self._unit_id_dict[unit_str]
		else:
			sys.stderr.write('Unitががありません\n')
			sys.exit(1)


def main():
	reader = UnitReader('unit_table.txt')
	minute = reader.get_criterion(u'分')
	hour = reader.get_criterion(u'時')
	value = 120 * (hour / minute)
	value = float(value)
	if value.is_integer(): value = int(value)
	
	from util import Util
	Util.dump(reader.unit_dict)
	print type(value), value

	return 0


if __name__ == '__main__':
	sys.exit(main())
