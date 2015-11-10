#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
# UnitX: 
#
#


class MainParser:
	"""
	【BNF for Numlang】
	<program>		::= <statements>
	<statements>	::= <eof> | <newlines> | <statement> <newlines> | <statement> <newlines> <statements>
	<statement>		::= <assign> | <print>
	<newlines>		::= '\n' | '\n' <newlines>
	<assign>		::= <variables> '=' <expression>
	<print>			::= "print" <expression>	
	<expression>	::= <expression> '+' <term> | <expression> '-' <term> | <term>
	<term>			::= <term> '*' <factor> | <term> '/' <factor> | <factor>				
	<factor> 		::= <variable> | <constant>* <unit> | '(' <expression> ')'
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
		import codecs
		self.num_file = codecs.open(filepath,'r', 'utf-8')
		#self.lines = self.num_file.read()
		self.lines = u"""\
a
a
a
a"""
	
	def __del__(self):
		self.num_file.close()

	def next_char(self):
		return self.code_iter.next().encode('utf-8') #str

	def program(self, index):
		self.statements(index)
		
	def statements(self, index):
		if self.is_end_of_file(index):
			pass
		elif self.is_newlines(index):
			index = self.newlines(index)
		else:
			print self.statement(index)
			index = self.next_newlines(index)
			print index
			#self.statements(index)

	def statement(self, index):
		res = self.lines[index]
		assert res == 'a'
		index+=1
		return res

	def is_newlines(self, index):
		next_index = self.next_newlines(index)
		assert next_index >= index # next_indexがマイナスならエラー
		return next_index > index
		
	def next_newlines(self, index):
		#print "next_newlines",index
		if self.lines[index] == '\n':
			index+=1
			return self.next_newlines(index)
		else:
			return index

	def is_end_of_file(self, index):
		index+=1
		return index >= len(self.lines)

	def assign(self, index):
		pass

	def print_(self, index):
		pass

	def expression(self, index):
		pass

	def term(self, index):
		pass

	def factor(self, index):
		pass

	def variable(self, index):
		pass

	def constant(self, index):
		pass

	def unit(self, index):
		pass

	def unit_operator(self, index):
		pass

	def id(self, index):
		pass

	def integer(self, index):
		pass

	def realr(self, index):
		pass
	
	def newline(self, index):
		pass

	def parse(self):
		index = 0
		self.program(index)
		print index

