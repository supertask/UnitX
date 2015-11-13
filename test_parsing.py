#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import parser

class ParsingTest():
	def __init__(self):
		import sys
		#if len(sys.argv) < 2: sys.exit(1)
		a_filepath = "test/test_code_0.num" #sys.argv[1]
		self.parser = parser.MainParser(a_filepath)


	def test_constant(self):
		test_lines = 		["12.5", "1521.", ".5", "55", "99.9aaa"]
		test_res_lines =	[12.5, 1521., .5, 55, 99.9]
		for test_line, test_res_line in zip(test_lines, test_res_lines):
			self.parser.index=0
			self.parser.lines = test_line
			res = self.parser.constant()
			assert res == test_res_line
			assert type(res) == type(test_res_line)

	def test_is_char_for_variable(self):
		test_lines = 		["", "SSFEFE", "aaa22", "22ge"]
		for test_line in test_lines:
			for a_char in test_line:
				print a_char, self.parser.is_char_for_variable(a_char)
			print

	
	def test_variable(self):
		test_lines = [u'あああ',u'aa']
		test_res_lines = test_lines
		for test_line, test_res_line in zip(test_lines, test_res_lines):
			self.parser.index=0
			self.parser.lines = test_line
			res = self.parser.variable()
			#print res.encode('utf-8')
			#assert res == test_res_line
			

	def setUp(self):
		print "Check.."

	def tearDown(self):
		print "OK"
		
if __name__ == "__main__":
	app = ParsingTest()
	app.setUp()
	#app.test_constant()
	app.test_variable()
	app.tearDown()
    #unittest.main()
