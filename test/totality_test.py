#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unitx_object_test import UnitXObjectTest
from each_syntax_test import EachSyntaxTest

def test():
	test_suite = unittest.TestSuite()
	test_suite.addTests(unittest.makeSuite(UnitXObjectTest))
	test_suite.addTests(unittest.makeSuite(EachSyntaxTest))

	return test_suite
