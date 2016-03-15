#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
"""

import sys

from antlr4 import *
from UnitXVisitor import UnitXVisitor
from UnitXParser import UnitXParser
from UnitXLexer import UnitXLexer

from unitx_object import UnitXObject
from unitx_object_calc import UnitXObjectCalc
from scope import Scope
from util import Util
from constants import Constants

class UnitXEvalVisitor(UnitXVisitor):
	
	def __init__(self):
		""" UnitXEvalVisitorを初期化して応答する．
		"""
		self.is_break = False
		self.scopes = []
		self.scopes.append(Scope(parent=None))
		UnitXObject.scopes = self.scopes
		self.calc = UnitXObjectCalc(self.scopes)

	# Visit a parse tree produced by UnitXParser#program.
	def visitProgram(self, ctx):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#typeDeclaration.
	def visitTypeDeclaration(self, ctx):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by UnitXParser#functionDeclaration.
	def visitFunctionDeclaration(self, ctx):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#formalParameters.
	def visitFormalParameters(self, ctx):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#formalParameterList.
	def visitFormalParameterList(self, ctx):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#formalParameter.
	def visitFormalParameter(self, ctx):
		return self.visitChildren(ctx)
		
	def __new_scope(self):
		"""現在のスコープ内のメモリを確保する．
		"""
		self.scopes.append(Scope(self.scopes[-1]))
		return

	def __del_scope(self):
		""" 現在のスコープ内のメモリを解放する．
		"""
		self.scopes.pop()
		return


	def visitBlock(self, ctx):
		"""
		for a_statement in ctx.blockStatement():
			if is_happened_break: break
			unitx_objs.append(self.visitExpression(an_expr))
		"""
		a_grandparent = ctx.parentCtx.parentCtx
		is_special_block = (isinstance(a_grandparent, UnitXParser.RepStatementContext) or isinstance(a_grandparent, UnitXParser.IfStatementContext) or isinstance(a_grandparent, UnitXParser.FunctionDeclarationContext))

		if is_special_block:
			self.visitChildren(ctx)
		else:
			self.__new_scope()
			self.visitChildren(ctx)
			self.__del_scope()
		return 


	# Visit a parse tree produced by UnitXParser#blockStatement.
	def visitBlockStatement(self, ctx):
		return self.visitChildren(ctx)


	def visitStatement(self, ctx):
		""" それぞれの文を辿って，応答する．
		"""
		#print Util.dump(self.scopes)
		if ctx.block(): self.visitBlock(ctx.block())
		elif ctx.repStatement(): self.visitRepStatement(ctx.repStatement())
		elif ctx.ifStatement(): self.visitIfStatement(ctx.ifStatement())
		elif ctx.expressionStatement(): self.visitExpressionStatement(ctx.expressionStatement())
		elif ctx.returnStatement(): self.visitReturnStatement(ctx.returnStatement()) #still
		elif ctx.start.type == UnitXLexer.BREAK: pass #still
		elif ctx.start.type == UnitXLexer.CONTINUE: pass #still
		elif ctx.printStatement(): self.visitPrintStatement(ctx.printStatement())
		elif ctx.dumpStatement(): self.visitDumpStatement(ctx.dumpStatement()) #still
		elif ctx.borderStatement(): self.visitBorderStatement(ctx.borderStatement())
		else:
			raise Exception("Syntax error. UnitXEvalVisitor#visitStatement") # Never happen.
		return


	def visitBorderStatement(self, ctx):
		""" 線を出力して応答する．
			ex: ---, ----, -----
		"""
		print ctx.start.text
		return


	# Visit a parse tree produced by UnitXParser#repStatement.
	def visitRepStatement(self, ctx):
		""" 与えられた回数の繰り返し処理を実行し，応答する．
			また，繰り返し処理の前にスコープのメモリ領域を確保し，繰り返し処理の後にそのスコープのメモリ領域を解放する．すなわち，スコープを管理する．
			ex: rep(i,5){...}, rep(i,[1,2,3]){...}, rep(i,[{B},{KB},{MB}])
		"""
		var_obj, end_control = self.visitRepControl(ctx.repControl())
		end_value = end_control.get_value()
		if isinstance(end_value, int): repeat_list = [UnitXObject(value=x,varname=None) for x in range(end_value)]
		else: repeat_list = end_value
		self.__new_scope()
		for i in repeat_list:
			# var_obj: 変数名=O,値=X，i: 変数名=X,値=O
			self.calc.assign(var_obj, i) # i=UnitXObject
			self.visitStatement(ctx.statement())
		self.__del_scope()
		return


	# Visit a parse tree produced by UnitXParser#ifStatement.
	def visitIfStatement(self, ctx):
		return self.visitChildren(ctx)

	def visitExpressionStatement(self, ctx): return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#returnStatement.
	def visitReturnStatement(self, ctx):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#printStatement.
	def visitPrintStatement(self, ctx):
		unitx_strs = [str(self.visitExpression(an_expr).get_value()) for an_expr in ctx.expression()]
		print ' '.join(unitx_strs)
		return


	# Visit a parse tree produced by UnitXParser#dumpStatement.
	def visitDumpStatement(self, ctx):
		unitx_strs = []
		for an_expr in ctx.expression():
			unitx_obj = self.visitExpression(an_expr)
			varname = unitx_obj.get_varname(error=False) #変数に格納されていない値もdumpで見るため
			if varname:
				unitx_strs.append("%s: %s" % (varname, unitx_obj.get_value()))
			else:
				unitx_strs.append("%s" % unitx_obj.get_value())
		print ' '.join(unitx_strs)
		return		

	# Visit a parse tree produced by UnitXParser#expressionList.
	def visitExpressionList(self, ctx):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#parExpression.
	def visitParExpression(self, ctx):
		return self.visitChildren(ctx)


	def visitRepControl(self, ctx):
		""" Visit a parse tree produced by UnitXParser#repControl.
			ex: [i,5], [i,[1,2,3]]
		"""
		varname = ctx.Identifier().getText()
		return [UnitXObject(value=None, varname=varname), self.visitEndRep(ctx.endRep())]


	def visitEndRep(self, ctx):
		""" 
			It checks a value of expr to be able to cast by int().
		"""
		if ctx.expression():
			an_expr = self.visitExpression(ctx.expression())
			# You must check value of expr to be able to cast by int().
			return an_expr


	def visitExpression(self, ctx):
		""" UnitXObject同士を計算した結果を返す．
			return: UnitXObject
		"""
		if ctx.expression(i=0):
			# x,y: UnitXObject
			x = self.visitExpression(ctx.expression(i=0))

			if ctx.start.type == UnitXLexer.INC: res = self.calc.increment(x)
			elif ctx.start.type == UnitXLexer.DEC: res = self.calc.decrement(x)
			else:
				y = self.visitExpression(ctx.expression(i=1))
				#print y.dump_both()
				an_operator = ctx.getChild(i=1).getSymbol()
				if an_operator.type == UnitXLexer.ADD: res = self.calc.add(x,y)
				elif an_operator.type == UnitXLexer.SUB: res = self.calc.subtract(x,y)
				elif an_operator.type == UnitXLexer.MUL: res = self.calc.multiply(x,y)
				elif an_operator.type == UnitXLexer.DIV: res = self.calc.divide(x,y)
				elif an_operator.type == UnitXLexer.ASSIGN: res = self.calc.assign(x,y)
				elif an_operator.type == UnitXLexer.ADD_ASSIGN: res = self.calc.add_assign(x,y)
				elif an_operator.type == UnitXLexer.SUB_ASSIGN: res = self.calc.substract_assign(x,y)
				elif an_operator.type == UnitXLexer.MUL_ASSIGN: res = self.calc.multiply(x,y)
				elif an_operator.type == UnitXLexer.DIV_ASSIGN: res = self.calc.divide(x,y)
				elif an_operator.type == UnitXLexer.MOD_ASSIGN: res = None
				else: res = None
		elif ctx.primary(): res = self.visitPrimary(ctx.primary())
		else:
			raise Exception("Syntax error. UnitXEvalVisitor#visitExpression") # Never happen.
		assert(isinstance(res, UnitXObject) or isinstance(res, None))

		return res

	# Visit a parse tree produced by UnitXParser#unit.
	def visitUnit(self, ctx):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#unitSingleOrPairOperator.
	def visitUnitSingleOrPairOperator(self, ctx):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#unitOperator.
	def visitUnitOperator(self, ctx):
		return self.visitChildren(ctx)


	def visitPrimary(self, ctx):
		""" それぞれのPrimaryの値をUnitXObjectにラップして，応答する．

			Identifier: variable or function
			literal: number, string, boolean, none
			PAREN=(): expression
			BRACK=[]: list
		"""
		if ctx.Identifier(): res = UnitXObject(value=None, varname = ctx.Identifier().getText())
		elif ctx.literal():
			a_value = self.visitLiteral(ctx.literal())
			if a_value is None: res = None
			else: res = UnitXObject(value=a_value, varname=None)
		elif ctx.start.type == UnitXLexer.LPAREN:
			res = self.visitExpression(ctx.expression(i=0))
		elif ctx.start.type == UnitXLexer.LBRACK:
			unitx_objs = [self.visitExpression(an_expr) for an_expr in ctx.expression()]
			return UnitXObject(value = unitx_objs, varname = None)
		else: raise Exception("Syntax error. UnitXEvalVisitor#visitPrimary") # Never happen.

		assert(isinstance(res, UnitXObject) or isinstance(res, None))
		return res


	def visitLiteral(self, ctx):
		""" それぞれのリテラルごとのvisitメソッドを呼び出し，その結果の値を応答する．
		"""
		if ctx.number(): return self.visitNumber(ctx.number())
		elif ctx.string(): return self.visitString(ctx.string())
		elif ctx.boolean(): return self.visitBoolean(ctx.boolean())
		elif ctx.none(): return None
		else: raise Exception("Syntax error. UnitXEvalVisitor#visitLiteral") # Never happen.


	def visitString(self, ctx):
		""" 文字列から，両端にあるダブルクォーテーション(\")，シングルクォーテーション(\')，トリプルダブルクォーテーション(\"\"\")，トリプルシングルクォーテーション(\'\'\')を排除し，応答する．
		"""
		a_value = ctx.start.text.strip('"\'')
		return a_value


	def visitNumber(self, ctx):
		""" 文字列から，int型,float型,複素数型へ変換し，応答する．
		"""
		if ctx.integer(): a_value = self.visitInteger(ctx.integer())
		elif ctx.FLOAT_NUMBER(): a_value = float(ctx.FLOAT_NUMBER().getText())
		elif ctx.IMAG_NUMBER(): a_value = complex(ctx.IMAG_NUMBER().getText())
		return a_value


	def visitInteger(self, ctx):
		""" 文字列からその文字列に属する進数へint変換し，応答する．
			変換する進数は，2,8,10,16進数．
		"""
		if ctx.DECIMAL_INTEGER(): a_value = int(ctx.DECIMAL_INTEGER().getText(),10)
		elif ctx.OCT_INTEGER(): a_value = int(ctx.OCT_INTEGER().getText(),8)
		elif ctx.HEX_INTEGER(): a_value = int(ctx.HEX_INTEGER().getText(),16)
		elif ctx.BIN_INTEGER(): a_value = int(ctx.BIN_INTEGER().getText(),2)
		return a_value


	def visitBoolean(self, ctx):
		""" 文字列からbooleanへ変換し，応答する．
		"""
		a_value = True if ctx.start.type == 'true' else False
		return a_value

