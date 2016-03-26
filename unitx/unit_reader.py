#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class UnitReader(object):
	""" 単位の情報を読み取り保存するクラス．
	"""

	def __init__(self, filename):
		""" UnitReaderの初期化
		"""
		self.filename = filename
		self.unit_id_dict = {}
		self.unit_evals = []

	def read(self):
		with open(self.filename) as rf:
			unit_id = 0
			line = rf.readline()
			while line:
				if line.rstrip() == '--':
					key_line = rf.readline().rstrip()
					unit_eval = rf.readline().rstrip()
					tokens = key_line.split()
					for a_token in tokens:
						a_token = a_token.decode('utf-8')
						self.unit_id_dict[a_token] = unit_id
					self.unit_evals.append(unit_eval)
					unit_id +=1
				line = rf.readline()


	def update_unit_dict(self, unit_str):
		print self.unit_id_dict
		print self.unit_evals
		

	def get_unit_id(self, unit_str):
		if unit_str in self.unit_id_dict:
			return self.unit_id_dict[unit_str]
		else:
			return -1



def main():
	reader = UnitReader('unit_table.txt')
	reader.read()

	return 0


if __name__ == '__main__':
	sys.exit(main())
