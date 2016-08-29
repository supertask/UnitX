#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Constants(object):
	"""A class defining a fixed numer for some classes."""

	#
	# Exit statuses
	#
	EXIT_SUCCESS = 0
	EXIT_FAILURE = 1
	EXIT_FAILURE_IN_UNITX = 44

	#
	# Unit databases
	#
	SYSTEM_UNIT_DATA = 'data/unit_table.dat'

	#
	# Error names
	#
	SYNTAX_ERR_RETURN_OUTSIDE = "SyntaxError: 'return' outside function"
	SYNTAX_ERR_BREAK_OUTSIDE = "SyntaxError: 'break' outside loop"

	NAME_ERR = "NameError: name '%s' is not defined."
	TYPE_ERR = "TypeError: cannot translate from '%s' to '%s'"
	TYPE_ERR_UNSUPPORTED_VALUE = "TypeError: unsupported operand for %s: '%s' and '%s'"
	TYPE_ERR_UNSUPPORTED_UNIT = "TypeError: unsupported operand for %s: unit '%s' and unit '%s'"
	TYPE_ERR_ARGS = "TypeError: %s() takes exactly %s arguments (%s given)"

	ASSERT_ERR = "AssertionError"
	EXPECT_ERR = "ExpectError: '%s' didn't coincide with '%s'."

	
def main():
	"""Run an example for a Constants class."""
	print Constants.EXIT_SUCCESS
	print Constants.EXIT_FAILURE

	print Constants.SYSTEM_UNIT_DATA

	print Constants.SYNTAX_ERR_RETURN_OUTSIDE
	print Constants.SYNTAX_ERR_BREAK_OUTSIDE

	print Constants.NAME_ERR % 'x'
	print Constants.TYPE_ERR % ('km','yen') #Here
	print Constants.TYPE_ERR_UNSUPPORTED_VALUE % ('x','x','x') #Here
	print Constants.TYPE_ERR_UNSUPPORTED_UNIT % ('x','x','x') #Here
	print Constants.TYPE_ERR_ARGS % ('test',2,1)

	print Constants.ASSERT_ERR
	print Constants.EXPECT_ERR % (1,2)

	return Constants.EXIT_SUCCESS

if __name__ == '__main__':
	sys.exit(main())
