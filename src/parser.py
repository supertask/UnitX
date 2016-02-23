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
	<statement>		::=  <debug> | <print> | <assign>
	<newlines>		::= '\n' | '\n' <newlines>
	<assign>		::= <variable> '=' <expr>
	<print>			::= <PRINT> <expr>
	<debug>			::= <DEBUG> <assign> | <DEBUG> <expr>
	<expr>			::= <term> [('+'|'-') <term> ]*
	<term>			::= <factor> [ ('*'|'/') <factor> ]*
	<factor> 		::= <variable> | <constant>* <unit> | '(' <expr> ')'
	<variable> 		::= <id>
	<constant> 		::= <INTEGER> | <REAL> 
	<unit>			::= '{' <unit_operator> '}'
	<unit_opeator>	::= <id> '/' <id> | <id> '->' <id> | '->' <id> | <id>
	<id> 			::= [a-zA-Z_][a-zA-Z0-9_]*
	<INTEGER> 		::= [0-9]+
	<REAL> 			::= [0-9]* "." [0-9]+
	<EOF>			::= EOF
	"""

	def __init__(self, filepath):
		import re
		self.float_ptr = re.compile('^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z')
		self.num_file = open(filepath,'r')
		self.lines = self.num_file.read()
		self.lines = self.lines.decode('utf-8')
		self.index = 0
		self.lines = """\
aa=2
ba=5
"""
		self.lines = self.lines.decode('utf-8')
		#self.root = None 
		#self.parser_rule = (statements, statement, newlines, assign, print_, debug, expr, term, factor, variable, constant, unit, unit_operator, EOF) = range(14)
		self.dict_of_global_var = {}
		self.dict_of_local_var = {}
	
	def __del__(self):
		self.num_file.close()

	def get_wchar(self):
		if self.is_EOF(): return None
		return self.get_wchar_of(self.index)

	def get_wchar_of(self, current_index):
		return self.lines[current_index]

	def next_char(self):
		""" どこのメソッドも使わない
		"""
		return self.code_iter.next().encode('utf-8') #str

	def add_one_index(self):
		""" 1増加させたindexがEOFかを返す
		"""
		assert not self.is_EOF()
		self.index+=1

	def is_next_EOF(self, d_index=1):
		return self.index + d_index >= len(self.lines)

	def is_EOF(self):
		return self.index >= len(self.lines)

	def is_newlines(self):
		next_index = self.guess_newlines(self.index)
		assert next_index >= self.index # next_indexがマイナスならエラー
		return next_index > self.index

	def newlines(self):
		self.index = self.guess_newlines(self.index)
		
	def guess_newlines(self, next_index):
		if self.is_next_EOF(d_index=next_index): return next_index
		elif self.lines[next_index] == '\n':
			next_index+=1
			return self.guess_newlines(next_index)
		else:
			return next_index
	
	def program(self):
		self.statements()
		
	def statements(self):
		#self.root = Node(, None)
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
		""" 1行の文字列解釈する
		"""
		#print self.get_wchar().encode('utf-8')
		if self.is_print_(): self.print_()
		else: self.assign() # Bug(11/26/2015), assignでなく、空文字がここに来る
		#self.add_one_index()
	

	def assign(self):
		""" 変数を代入する.
			Test: Good (11/20/2015)
		"""
		var_name = ''
		var_name = self.variable()
		assert self.get_wchar() == Lex.EQUAL
		self.add_one_index()
		a_constant = self.expr()
		self.dict_of_global_var[var_name] = a_constant

	def is_assign(self):
		self.assign()

	def is_print_(self):
		return self.lines[self.index:len(Lex.PRINT)] == Lex.PRINT

	def print_(self):
		""" 出力する引数をprintする
		"""
		self.index += len(Lex.PRINT)
		print self.expr()

	def is_wchar(self, a_char):
		if ord(a_char) >= 128: return True
		if a_char.isalpha(): return True
		return a_char == '_'

	def expr(self):
		""" 四則演算をする.
			@return int or float 定数

			Test: Good (11/20/2015)
		"""
		value = self.term();
		while (self.get_wchar() == Lex.ADD or self.get_wchar() == Lex.SUBTRACT):
			two_arithme_ope = self.get_wchar()
			self.add_one_index()
			if two_arithme_ope == Lex.ADD: value += self.term();
			else: value -= self.term();
		return value

	def term(self):
		""" 四則演算をする.
			@return int or float 定数

			Test: Good (11/20/2015)
		"""
		value = self.factor();
		while (self.get_wchar() == Lex.MULTIPLY or self.get_wchar() == Lex.DIVIDE):
			two_arithme_ope = self.get_wchar()
			self.add_one_index()
			if two_arithme_ope == Lex.MULTIPLY: value *= self.factor();
			else: value /= self.factor();
		return value

	def factor(self):
		""" 四則演算をする.
			@return int or float 定数

			Test: Bug (11/20/2015)
		"""
		a_constant = 0
		if self.get_wchar().isdigit():
			a_constant = self.constant()
		elif self.get_wchar() == Lex.LPAR:
			self.add_one_index()
			a_constant = self.expr()
			assert self.get_wchar() == Lex.RPAR
			self.add_one_index()
		else:
			a_constant = self.variable()
			value = self.dict_of_global_var[a_constant]
		return a_constant


	def variable(self):
		""" 変数をコードから取り出し返す。尚、変数はASCII以外も使用可能
			@return string 変数名

			Test: Good (11/19/2015)
		"""
		var_name = ''
		if self.is_wchar(self.get_wchar()):
			var_name += self.get_wchar()
			self.add_one_index()
		else:
			print 'syntax error.'
			sys.exit(1)
			#raise #after <-後から改善（エラーの内容をどうするか）
		while self.is_wchar(self.get_wchar()) or self.get_wchar().isdigit():
			var_name += self.get_wchar()
			self.add_one_index()

		return var_name

	def constant(self):
		""" 文字列表記の定数をコードから取り出し、その文字列表記の定数のを数値へ変換し、返す
			@return int or float 定数

			Test: Good (11/19/2015)
		"""
		number_str = ''
		if self.get_wchar() == '.':
			self.add_one_index()
			number_str='.'
		assert self.float_ptr.match(self.get_wchar())
		while True:
			if self.is_EOF(): break
			number_str += self.get_wchar()
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

