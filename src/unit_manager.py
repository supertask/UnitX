#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
from collegue import Collegue
from util import Util
from constants import Constants

class UnitManager(Collegue):
	""" A class parsing/saving unit informations from databases

	Attributes:
		ex_numer: A string indicating a numer of unit which used in the past.
	"""

	def __init__(self, filename):
		"""Inits attributes of a Unit class."""
		self.filename = filename
		self.prepare_exec = ""
		self.unit_dict = {}
		self.unit_evals = []
		self.__unit_id_dict = {}
		self.__is_updated = []
		self.__parse(self.filename)

	def __parse(self, filename):
		"""
		"""
		with codecs.open(filename, 'r', encoding='utf-8') as rf:
			line = rf.readline()
			while line:
				line = line.lstrip().rstrip()
				if line == 'prepare': self.__parse_prepare(rf)
				elif line == 'tokens': self.__parse_tokens(rf)
				else: pass
				line = rf.readline()

	def __parse_tokens(self, rf):
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
					self.__unit_id_dict[a_token] = unit_id
				self.unit_evals.append(dict_line)
				self.__is_updated.append(False)
				unit_id += 1
			line = rf.readline()
		return

	def __parse_prepare(self, rf):
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


	def __update_dict(self, unit_str, unit):
		"""
		"""
		unit_id = self.get_unit_id(unit_str, unit)
		if self.__is_updated[unit_id]:
			return
		adding_dict = eval(self.unit_evals[unit_id])
		if isinstance(adding_dict, dict):
			self.unit_dict.update(adding_dict)
			self.__is_updated[unit_id] = True
		return
		

	def get_criterion(self, unit_str, unit):
		"""
		"""
		self.__update_dict(unit_str, unit)
		return self.unit_dict[unit_str]


	def get_unit_id(self, unit_str, unit):
		"""
		"""
		if unit_str in self.__unit_id_dict:
			return self.__unit_id_dict[unit_str]
		else:
			msg = Constants.NAME_ERR % unit_str
			self.mediator.get_parser().notifyErrorListeners(msg, unit.token, Exception(msg))

	def set_mediator(self, mediator):
		self.mediator = mediator

def main():
	"""Run an example for a Unit class."""

	from simulator import Simulator
	s = Simulator()
	manager = s.get_manager()

	minute = manager.get_criterion(u'分')
	hour = manager.get_criterion(u'時')
	value = 120 * (hour / minute)
	
	Util.dump(manager.unit_dict)
	print u'kind of unit:', manager.get_unit_id(u'分')
	print '%s分' % value
	print '-' * 10

	from unit import Unit
	print manager._trans_original_value(u"10:00 - 17:00", Unit(u'US_Eastern', u'Asia_Tokyo'))

	return Constants.EXIT_SUCCESS


if __name__ == '__main__':
	sys.exit(main())
