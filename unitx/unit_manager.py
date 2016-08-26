#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
from collegue import Collegue
from util import Util

class UnitManager(Collegue):
	""" 単位の情報を読み取り保存するクラス．
	"""

	def __init__(self, filename):
		""" UnitManagerの初期化
		"""
		self.filename = filename
		self.prepare_exec = ""
		self.unit_dict = {}
		self._unit_id_dict = {}
		self._unit_evals = []
		self._is_updated = []
		self._parse(self.filename)

	def _parse(self, filename):
		"""
		"""
		with codecs.open(filename, 'r', encoding='utf-8') as rf:
			line = rf.readline()
			while line:
				line = line.lstrip().rstrip()
				if line == 'prepare': self._parse_prepare(rf)
				elif line == 'tokens': self._parse_tokens(rf)
				else: pass
				line = rf.readline()

	def _parse_tokens(self, rf):
		"""
		"""
		unit_id = 0
		line = rf.readline()
		while line:
			line = line.lstrip().rstrip()
			if line == 'end': return
			if line:
				token_line, dict_line = line.split('->')
				token_line = token_line.strip()
				dict_line = dict_line.strip()
				tokens = token_line.split()
				for a_token in tokens:
					self._unit_id_dict[a_token] = unit_id
				self._unit_evals.append(dict_line)
				self._is_updated.append(False)
				unit_id += 1
			line = rf.readline()
		return

	def _parse_prepare(self, rf):
		"""
		"""
		line = rf.readline()
		self.prepare_exec = ""
		while line:
			line = line.rstrip()
			if line == 'end':
				exec(self.prepare_exec, globals())
				return
			self.prepare_exec += line+'\n'
			line = rf.readline()
		return


	def get_prepare_exec(self):
		return self.prepare_exec


	def _update_dict(self, unit_str, unit):
		"""
		"""
		unit_id = self.get_unit_id(unit_str, unit)
		if self._is_updated[unit_id]:
			return
		adding_dict = eval(self._unit_evals[unit_id])
		if isinstance(adding_dict, dict):
			self.unit_dict.update(adding_dict)
			self._is_updated[unit_id] = True
		return
		

	def get_criterion(self, unit_str, unit):
		"""
		"""
		self._update_dict(unit_str, unit)
		return self.unit_dict[unit_str]


	def get_unit_id(self, unit_str, unit):
		"""
		"""
		if unit_str in self._unit_id_dict:
			return self._unit_id_dict[unit_str]
		else:
			msg = "NameError: is not defined '%s' in this lang" % unit_str
			self.mediator.get_parser().notifyErrorListeners(msg, unit.token, Exception(msg))

	def set_mediator(self, mediator):
		self.mediator = mediator

def main():
	manager = UnitManager('data/unit_table.dat')
	minute = manager.get_criterion(u'分')
	hour = manager.get_criterion(u'時')
	value = 120 * (hour / minute)
	
	Util.dump(manager.unit_dict)
	print u'kind of unit:', manager.get_unit_id(u'分')
	print '%s分' % value
	print '-' * 10

	from unit import Unit
	print manager._trans_original_value(u"10:00 - 17:00", Unit(u'US_Eastern', u'Asia_Tokyo'))

	return 0


if __name__ == '__main__':
	sys.exit(main())
