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
	"""A class running a parser on each mode.

	Attributes:
		is_intaractive_run: A bool indicating whether an intaractive mode.
		stock_line: A string stocking a code which is a block statement
			on the intaractive mode.
		errhandler: An instance of EvalErrorStrategy for reporting all errors.
		visitor: An instance of EvalVisitor called by a parser.
		parser: An instance of UnitXParser for parsing codes.
		Cmd.prompt: A string displaying against every code line.
	"""

	#
	# A string displaying against every code line.
	#
	Cmd.prompt = 'unitx> '

	def __init__(self, is_intaractive_run):
		"""Inits attributes of a Unit class."""
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
		"""Executes demo programs. This is called, when 'demo' is typed by a user.

		Args:
			arg_line: A string which is given by a user.
		"""
		if arg_line.isdigit(): print "Xdemo", int(arg_line)
		else: pass #error


	def do_help(self, arg_line):
		"""Prints a help. This is called, when 'help' is typed by a user.

		Args:
			arg_line: A string which is given by a user.
		"""
		print "I don't help you."
	

	def do_quit(self, arg_line):
		"""Quits this program. This is called, when 'quit' is typed by a user.

		Args:
			arg_line: A string which is given by a user.
		"""
		sys.exit(Constants.EXIT_SUCCESS)

	def do_EOF(self, arg_line):
		"""Prints a new line for a new command line. This is called, when <ctrl+D> or <EOF> are called by a user.

		Args:
			arg_line: A string which is given by a user.
		Returns:
			A bool whether this function is called the 
		"""
		print
		return True
	

	def emptyline(self):
		"""Executes a code when '\n' is typed by a user."""
		self.talk('' + '\n')

	def default(self, a_line):
		"""Executes a code when there is a string, except a command string
			which is defined in this class.

		Attributes:
			a_line: a string which is typed by a user, except a command stirng
				which is defined in this class.
		"""
		self.talk(a_line + '\n')


	def talk_loop(self):
		"""Repeatedly issue a prompt, accept input, parse an initial prefix off the received input, and dispatch to action methods, passing them the remainder of the line as argument."""
		try: Cmd.cmdloop(self)
		except KeyboardInterrupt as e:
			print 'KeyboardInterrupt!'
			self.talk_loop()
		return
		

	def eat_code(self, a_path):
		"""Executes a code indicated as a_path on the IO mode.
		
		In this version, we just support UTF-8. As the next vision, we need to support UTF-8.

		Attributes:
			a_path: a string indicating a path of the source code.
		"""
		self.visitor.get_errlistener().set_codepath(a_path)
		a_stream = FileStream(a_path, encoding='utf-8')
		self.parse(a_stream)
		return


	def talk(self, a_line):
		"""Executes a code indicated as a_path on the IO mode.
		
		In this version, we just support UTF-8. As the next vision, we need to support UTF-8.

		Attributes:
			a_line: a string which is typed by a user, except a command string
				which is defined in this class.
		"""
		if self.errhandler.is_ignored_block:
			# Errors of block statement never happen until coming empty char.
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
			Cmd.prompt = 'unitx> '
			self.stock_line = ""
		return


	def parse(self, a_stream):
		"""Parses a stream which is FileStream(the IO mode) or InputStream(the intaractive mode).

		Attributes:
			a_stream: an instance of FileStream(the IO mode) or InputStream(the intaractive mode).
		"""
		a_lexer = UnitXLexer(a_stream)
		token_stream = CommonTokenStream(a_lexer)
		self.parser.setTokenStream(token_stream)

		a_tree = self.parser.program() #Bug
		self.visitor.visit(a_tree)
		return


def main(argv):
	"""Run an example for a Unit class."""

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
