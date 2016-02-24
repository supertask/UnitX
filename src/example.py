#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
"""

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from UnitXLexer import UnitXLexer
from UnitXParser import UnitXParser
from unitx_walker import UnitXWalker

def parse_file(in_stream):
	"""
	"""
	a_lexer = UnitXLexer(in_stream)
	token_stream = CommonTokenStream(a_lexer)
	a_parser = UnitXParser(token_stream)
	a_tree = a_parser.program()
	a_listener = UnitXWalker()
	walker = ParseTreeWalker()
	walker.walk(a_listener, a_tree);
	lisp_tree_str = a_tree.toStringTree(recog=a_parser)
	return lisp_tree_str

def test_run(input_str):
	"""
	"""
	return parse_file(InputStream(input_str))

def main(argv):
	""" 
	"""
	if len(argv) > 1:
		print parse_file(FileStream(argv[1], encoding='utf-8'))
	else:
		while True:
			sys.stdout.write('>> ')
			print parse_file(InputStream(sys.stdin.readline()))
	return 0

if __name__ == '__main__':
	main(sys.argv)
