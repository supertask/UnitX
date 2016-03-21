#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
import sys
from unitx_object import UnitXObject

""" 複数のクラスを跨って必要な定数を定義する定義ファイル．
"""
class Constants(object):
	ZERO = UnitXObject(value=0, varname=None)
	ONE = UnitXObject(value=1, varname=None)
	
def main():
	print Constants.ZERO, Constants.ZERO.get_value()
	print Constants.ONE, Constants.ONE.get_value()
	return 0

if __name__ == '__main__':
	sys.exit(main())
