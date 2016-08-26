#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest
import subprocess
from unitx.example import Example

class Tester(unittest.TestCase):
	"""
	"""

	"""
	def __print(self, content):
		pass
	"""

	def __check_an_error(self, cmd, stdin, ans_code):
		p = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		_, stderr_data = p.communicate()
		with open(ans_code + '.tmp', 'w') as wf:
			wf.write(stderr_data)
		res = open(ans_code, 'r').read()
		assert(stderr_data == res) #エラーコードが一致していないとき例外を吐く
		p.wait()


	def test_errors_in_Intaractive(self):
		pass
		"""
		for a_code, ans_code in zip(self.err_codes,self.err_ans_codes):
			print 'Checking "%s" on intaractive mode' % a_code
			self.__check_an_error(["python","unitx/example.py"], open(a_code, 'r'), ans_code)
		"""


	def test_codes(self):
		for a_code in self.test_codes:
			print 'Checking "%s" on intaractive mode' % a_code
			self.cmd = Example(is_intaractive_run=True)
			self.cmd.visitor.is_test = True
			with open(a_code, 'r') as rf:
				for line in rf:
					self.cmd.talk(line)

			print 'Checking "%s" on IO mode' % a_code
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
					self.err_ans_codes.append(os.path.join('tests', name+'.ans'))
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
