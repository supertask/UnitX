#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
from unitx.example import Example

#
# return_code = subprocess.check_call(["unitx"])
#

def intaractive_test():
	cmd = Example()
	cmd.talk("aa = 5 + 2{USD}")
	cmd.talk("3 * 1{万}")

def code_test():
	pass

def test():
	print 'Start test.'
	intaractive_test()
	code_test()
	print 'End test.'


def main(argv):
	test()
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
