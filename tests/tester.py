#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
from unitx.example import Example

"""
Memo
return_code = subprocess.check_call(["unitx"])


"""

class Tester(unittest.TestCase):
	def test_intaractive_mode(self):
		cmd = Example()
		cmd.talk("aa = 5 + 2{USD} expect(aa, 7{USD})")
		cmd.talk("3 * 1{万} expect(aa, 7{USD})")

	def test_io_mode(self):
		cmd = Example()
		cmd.talk("aa = 4 + 2{USD}")
		cmd.talk("3 * 2{万}")
		#print os.listdir('.')

	def setUp(self):
		print

	def tearDown(self):
		pass

def main(argv):
	t = Tester()
	t.test()

	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))
