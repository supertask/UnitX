#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

"""
それぞれのシンタックスをテストするクラス．
"""
class EachSyntaxTest(unittest.TestCase):
	def test_print(self):
		from unitx.example import test_run
		left = test_run("""print 'a'""")
		print left
