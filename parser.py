#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
# UnitX: 
#
#


from lex import Lex
import sys

class MainParser:
	"""
	【BNF for Numlang】
	<program>		::= <statements>
	<statements>	::= <EOF> | <newlines> <statements> | <statement> <newlines> <statements>
	<statement>		::= <assign> | <print>
	<newlines>		::= '\n' | '\n' <newlines>
	<assign>		::= <variable> '=' <expr>
	<print>			::= <PRINT> <expr>	
	<expr>	::= <term> [('+'|'-') <term> ]*
	<term>			::= <factor> [ ('*'|'/') <factor> ]*
	<factor> 		::= <variable> | <constant>* <unit> | '(' <expr> ')'
	<variable> 		::= <id>
	<constant> 		::= <integer> | <real> 
	<unit>			::= '{' <unit_operator> '}'
	<unit_opeator>	::= <id> '/' <id> | <id> '->' <id> | '->' <id> | <id>
	<id> 			::= [a-zA-Z_][a-zA-Z0-9_]*
	<integer> 		::= [0-9]+
	<real> 			::= [0-9]* "." [0-9]+
	<none>			::= ''
	<eof>			::= EOF
	"""

	def __init__(self, filepath):
		import re
		self.float_ptr = re.compile('^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z')
		#import codecs
		#self.num_file = codecs.open(filepath,'r', 'utf-8')
		self.num_file = open(filepath,'r')
		self.lines = self.num_file.read()
		self.lines = self.lines.decode('utf-8')
		self.index = 0
		self.lines = """\
あ
い

う

え
お
"""
		self.lines = self.lines.decode('utf-8')
	
	def __del__(self):
		self.num_file.close()

	def next_char(self):
		""" どこのメソッドも使わない
		"""
		return self.code_iter.next().encode('utf-8') #str

	def add_index(self, i=1):
		if self.is_next_EOF():
			sys.exit(1)
		else:
			self.index+=1

	def add_one_index(self):
		self.add_index()

	def is_next_EOF(self):
		self.is_EOF(d_index=1)

	def is_EOF(self, corrent_index=-1, d_index=0):
		if corrent_index == -1: corrent_index = self.index
		return corrent_index + d_index >= len(self.lines)

	def program(self):
		self.statements()
		
	def statements(self):
		if self.is_EOF():
			pass
		elif self.is_newlines():
			self.newlines()
			self.statements()
		else:
			self.statement()
			self.newlines()
			self.statements()

	def statement(self):
		print self.lines[self.index].encode('utf-8')
		self.add_one_index()
		#if self.is_print_(): self.print_()
		#else: self.assign()
	
	def is_newlines(self):
		next_index = self.guess_newlines(self.index)
		assert next_index >= self.index # next_indexがマイナスならエラー
		return next_index > self.index

	def newlines(self):
		self.index = self.guess_newlines(self.index)
		
	def guess_newlines(self, next_index):
		if self.is_EOF(corrent_index=next_index): return next_index
		elif self.lines[next_index] == '\n':
			next_index+=1
			return self.guess_newlines(next_index)
		else:
			return next_index
	

	""" ここから未チェック
	"""

	def assign(self):
		self.variable()
		assert self.lines[self.index] == '='
		self.add_one_index()
		self.expr()

	def is_print_(self):
		return self.lines[self.index:len(Lex.PRINT)] == Lex.PRINT

	def print_(self):
		self.index += len(Lex.PRINT)
		self.expr()

	def is_char_for_variable(self, a_char):
		if ord(a_char) >= 128: return True
		if a_char.isalpha(): return True
		return a_char == '_'

	def variable(self):
		var_name = ""
		if self.is_char_for_variable(self.lines[self.index]):
			var_name += self.lines[self.index]
			self.add_one_index()
		while True:
			print var_name.encode('utf-8')
			if not self.is_char_for_variable(self.lines[self.index]):
				break
			if self.lines[self.index].isdigit():
				break
			var_name += self.lines[self.index]
			self.add_one_index()
		return var_name

	def expr(self):
		value = term();
		while (self.lines[self.index] == Lex.ADD or self.lines[self.index] == Lex.SUBTRACT):
			two_arithme_ope = self.lines[self.index]
			self.add_one_index()
			if two_arithme_ope == Lex.ADD: value += term();
			else: value -= term();
		return value

	def term(self):
		value = factor();
		while (self.lines[self.index] == Lex.MULTIPLY or self.lines[self.index] == Lex.DIVIDE):
			two_arithme_ope = self.lines[self.index]
			self.add_one_index()
			if two_arithme_ope == Lex.MULTIPLY: value *= factor();
			else: value /= factor();
		return value

	def factor(self):
		if isdigit(self.lines[self.index]):
			self.constant()
		elif self.lines[self.index] == Lex.LPAR:
			self.add_one_index()
			value = expr()
			assert self.lines[self.index] == Lex.RPAR
			self.add_one_index()
		else:
			var_name = variable()

	def constant(self):
		number_str = ''
		if self.lines[self.index] == '.':
			self.add_one_index()
			number_str='.'
		assert self.float_ptr.match(self.lines[self.index])
		while True:
			if self.is_EOF(): break
			number_str += self.lines[self.index]
			if not self.float_ptr.match(number_str):
				number_str = number_str[:-1]
				break
			self.add_one_index()
		if number_str.isdigit(): return int(number_str)
		else: return float(number_str)

	def unit(self):
		pass

	def unit_operator(self):
		pass

	def id(self):
		pass

	def integer(self):
		pass

	def realr(self):
		pass
	
	def newline(self):
		pass

	def parse(self):
		index = 0
		self.program()

