#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
import sys
from unitx_object import UnitXObject

class Constant:
	""" 複数のクラスを跨って必要な定数を定義するクラス．
	"""
	ZERO = UnitXObject(0)
	
def main():
	print Constant.ZERO.get_value()
	
	return 0

if __name__ == '__main__':
	sys.exit(main())
