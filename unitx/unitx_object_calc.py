#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from unitx_object import UnitXObject
from collegue import Collegue

class UnitXObjectCalc(Collegue):
	""" UnitXObject同士の値を計算するクラス．
	"""

	def __init__(self):
		""" scopesを設定して，応答する．
		"""
		pass



	def set_mediator(self, mediator):
		self.mediator = mediator

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
