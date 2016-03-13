#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

"""
単位(Unit)計算用のライブラリをテストするクラス．
"""
class UnitXObjectTest(unittest.TestCase):
	def test_add_unit(self):
		import unitx.unitx_parser
