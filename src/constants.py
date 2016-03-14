#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
import sys
from unitx_object import UnitXObject

""" 複数のクラスを跨って必要な定数を定義する定義ファイル．
"""
class Constants:
	ZERO = UnitXObject(0)
	ONE = UnitXObject(1)
	
def main():
	print Constants.ONE, Constants.ONE.get_value()
	print Constants.ZERO, Constants.ZERO.get_value()
	return 0

if __name__ == '__main__':
	sys.exit(main())
