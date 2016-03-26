#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Unit:
	""" 単位の情報を持つクラス．
		ex: {MB}, {kg->g}, {m/s}
	"""

	def __init__(self, ex_numer, numer, ex_denom, denom):
		""" Unitの初期化
		"""
		self.ex_numer = ex_numer
		self.ex_denom = ex_denom
		self.numer = numer
		self.denom = denom

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
