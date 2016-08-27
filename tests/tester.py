#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest
import subprocess
from unitx.example import Example
from unitx.constants import Constants

class Tester(unittest.TestCase):
	""" """

	def __check_a_bug(self, exit_status):
		"""Tag a bug.

		If exit_status is Constants.SUCCESS_FAILURE or Constants.EXIT_FAILURE_IN_UNITX,
		The UnitX system works normally. But if it's Constants.EXIT_FAILURE, it's going to be a bug.
		"""
		if exit_status == Constants.EXIT_FAILURE:
			print '-' * 50
			print 'A BUG IN UnitX(ERR_CODE=%s)' % Constants.EXIT_FAILURE
			print '-' * 50
			sys.exit(Constants.EXIT_FAILURE)


	def test_errors_in_Intaractive(self):
		for a_code in self.err_codes:
			print 'Checking "%s"(ERROR SOURCE) on intaractive mode' % a_code
			p = subprocess.Popen(["python","unitx/example.py"], stdin=open(a_code, 'r'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			exit_status = p.wait()
			self.__check_a_bug(exit_status)

			print 'Checking "%s"(ERROR SOURCE) on IO mode' % a_code
			p = subprocess.Popen(["python","unitx/example.py", a_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			exit_status = p.wait()
			self.__check_a_bug(exit_status)


	def test_codes(self):
		for a_code in self.test_codes:
			print 'Checking "%s"(CORRECT SOURCE) on intaractive mode' % a_code
			self.cmd = Example(is_intaractive_run=True)
			self.cmd.visitor.is_test = True
			with open(a_code, 'r') as rf:
				for line in rf:
					self.cmd.talk(line)
			print 'Checking "%s"(CORRECT SOURCE) on IO mode' % a_code
			self.cmd = Example(is_intaractive_run=False)
			self.cmd.visitor.is_test = True
			self.cmd.eat_code(a_code)
	
	def setUp(self):
		print
		self.test_codes = []
		self.err_codes = []
		self.err_ans_codes = []
		for filename in os.listdir('tests'):
			name, ext = os.path.splitext(filename)
			if ext == '.unit':
				if 'err' in name:
					self.err_codes.append(os.path.join('tests', filename))
				else:
					self.test_codes.append(os.path.join('tests', filename))

	def tearDown(self):
		pass


def main(argv):
	t = Tester()
	t.test()

	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))
