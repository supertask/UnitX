#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from UnitXLexer import UnitXLexer
from UnitXParser import UnitXParser
from eval_visitor import EvalVisitor
from eval_error_strategy import EvalErrorStrategy
from eval_error_listener import EvalErrorIOListener
from eval_error_listener import EvalErrorIntaractiveListener
from util import Util
from constants import Constants

from cmd import Cmd
import readline
import rlcompleter

class Example(Cmd):
	"""A class running a parser on each some mode.

	"""

	Cmd.prompt = 'unitx> '

	def __init__(self, is_intaractive_run):
		Cmd.__init__(self)
		self.is_intaractive_run = is_intaractive_run
		self.stock_line = ""
		self.errhandler = EvalErrorStrategy(self.is_intaractive_run)
		self.visitor = EvalVisitor(self.is_intaractive_run, self.errhandler)
		self.parser = UnitXParser(None)
		self.parser._errHandler = self.errhandler
		self.visitor.set_parser(self.parser)

		if is_intaractive_run:
			a_listener = EvalErrorIntaractiveListener(self.visitor)
		else:
			a_listener = EvalErrorIOListener(self.visitor)
		self.parser._listeners = [a_listener]
		self.visitor.set_errlistener(a_listener)


	def do_demo(self, arg_line):
		if arg_line.isdigit(): print "Xdemo", int(arg_line)
		else: pass #error

	def do_help(self, arg_line):
		print "I don't help you."
	
	def do_quit(self, arg_line):
		sys.exit(Constants.EXIT_SUCCESS)

	def do_EOF(self, arg_line):
		print
		return True
	
	def emptyline(self):
		self.talk('' + '\n')

	def default(self, a_line):
		self.talk(a_line + '\n')

	def talk_loop(self):
		try: Cmd.cmdloop(self)
		except KeyboardInterrupt as e:
			print 'KeyboardInterrupt!'
			self.talk_loop()
		

	def get_stream(self, a_line):
		return a_stream


	def eat_code(self, a_path):
		self.visitor.get_errlistener().set_codepath(a_path)
		a_stream = FileStream(a_path, encoding='utf-8')
		self.parse(a_stream)


	def talk(self, a_line):
		if self.errhandler.is_ignored_block:
			# Errors of block statement never happen until coming empty char
			if not a_line.strip():
				self.errhandler.is_ignored_block = False
			codeline = self.stock_line + a_line
		else:
			codeline = a_line

		codeline = codeline.decode('utf-8')
		lines = codeline.split('\n')
		self.visitor.get_errlistener().set_codelines(lines)

		a_stream = InputStream(codeline)
		self.parse(a_stream)

		if self.errhandler.is_ignored_block:
			Cmd.prompt = '...... '
			self.stock_line = self.stock_line + a_line
		else:
			#print self.stock_line
			Cmd.prompt = 'unitx> '
			self.stock_line = ""
		return


	def parse(self, a_stream):
		"""
		"""
		a_lexer = UnitXLexer(a_stream)
		token_stream = CommonTokenStream(a_lexer)
		self.parser.setTokenStream(token_stream)

		a_tree = self.parser.program() #Bug
		self.visitor.visit(a_tree)
		return


def main(argv):
	""" 
	"""
	if len(argv) > 1:
		cmd = Example(is_intaractive_run=False)
		cmd.eat_code(argv[1])
	else:
		cmd = Example(is_intaractive_run=True)
		import intro_line
		print intro_line.get_line()
		cmd.talk_loop()

	return Constants.EXIT_SUCCESS


if __name__ == '__main__':
	sys.exit(main(sys.argv))

