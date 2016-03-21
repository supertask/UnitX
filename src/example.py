#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
"""

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from UnitXLexer import UnitXLexer
from UnitXParser import UnitXParser
from eval_visitor import EvalVisitor
from eval_error import EvalError

class Example(object):
	"""
	"""

	def __init__(self, is_intaractive_run):
		"""
		"""
		self.errhandler = EvalError(is_intaractive_run)
		self.visitor = EvalVisitor(is_intaractive_run, self.errhandler)
		self.parser = UnitXParser(None)
		self.parser._errHandler = self.errhandler

	def parse(self, a_stream):
		"""
		"""
		a_lexer = UnitXLexer(a_stream)
		token_stream = CommonTokenStream(a_lexer)
		self.parser.setTokenStream(token_stream)
		a_tree = self.parser.program()
		self.visitor.visit(a_tree)
		return

	def talk(self):
		a_line, stock_line = "", ""
		while True:
			if self.errhandler.is_ignored_block: sys.stdout.write('...... ')
			else: sys.stdout.write('unitx> ')
			a_line = sys.stdin.readline()

			if self.errhandler.is_ignored_block:
				#
				# In block statement, Errors never happen until coming empty char,
				# because 'is_ignored_block' are written by EvalError class.
				#
				if not a_line.strip():
					self.errhandler.is_ignored_block = False
				a_stream = InputStream(stock_line + a_line)
			else: a_stream = InputStream(a_line)
			self.parse(a_stream)
			
			if self.errhandler.is_ignored_block: stock_line = stock_line + a_line
			else: stock_line = ""

	def test_run(input_str):
		"""
		"""
		return parse_inline(InputStream(input_str))


def main(argv):
	""" 
	"""
	if len(argv) > 1:
		an_example = Example(is_intaractive_run=False)
		a_stream = FileStream(argv[1], encoding='utf-8')
		an_example.parse(a_stream)
	else:
		an_example = Example(is_intaractive_run=True)
		an_example.talk()
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
