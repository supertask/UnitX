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
		self.ctxes = []
		self.scopes = []
		self.scopes.append(Scope(parent=None))
		self.calc = UnitXObjectCalc(self.scopes)
		self.is_break = False

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


	def visitStatement(self, ctx):
		""" Visit a parse tree produced by UnitXParser#statement.
		"""
		if ctx.block():
			parent_type = ctx.parentCtx.start.type
			if parent_type == UnitXLexer.REP or parent_type == UnitXLexer.IF:
				self.visitBlock(ctx.block())
			else:
				self.__new_scope()
				self.visitBlock(ctx.block())
				self.__del_scope()
			return

		elif ctx.start.type == UnitXLexer.REP:
			#
			# rep(i,5) or rep(i,[1,2,3])
			#
			var_obj, end_control = self.visitRepControl(ctx.repControl())
			end_value = end_control.get_value()
			if isinstance(end_value, int): repeat_list = [UnitXObject(x) for x in range(end_value)]
			else: repeat_list = end_value

			self.__new_scope()
			for i in repeat_list:
				self.calc.assign(var_obj, i)
				self.visitStatement(ctx.statement(i=0))
			self.__del_scope()

			return
		
		elif ctx.start.type == UnitXLexer.IF:
			pass
		elif ctx.start.type == UnitXLexer.PRINT:
			print self.visitExpression(ctx.expression())
			return

		elif ctx.start.type == UnitXLexer.RETURN:
			pass
		elif ctx.start.type == UnitXLexer.BREAK:
			pass

		elif ctx.start.type == UnitXLexer.CONTINUE:
			pass
		#elif ctx.start.type == UnitXLexer.E:
		#	print self.visitExpression(ctx.expression())
		#elif ctx.borderPrinter(): self.visitBorderPrinter(ctx.borderPrinter())
		#else: pass

		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#borderPrinter.
	def visitBorderPrinter(self, ctx):
		print ctx.start.text
		return None


	# Visit a parse tree produced by UnitXParser#block.
	def visitBlock(self, ctx):
		"""
		for a_statement in ctx.blockStatement():
			if is_happened_break: break
			unitx_objs.append(self.visitExpression(an_expr))
		"""
		return self.visitChildren(ctx)


	# Visit a parse tree produced by UnitXParser#blockStatement.
	def visitBlockStatement(self, ctx):
		return self.visitChildren(ctx)


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
		return [UnitXObject(varname, is_identifier=True), self.visitEndRep(ctx.endRep())]


	def visitEndRep(self, ctx):
		""" Visit a parse tree produced by UnitXParser#endRep.
			It checks a value of expr to be able to cast by int().
		"""
		if ctx.expression():
			expr = self.visitExpression(ctx.expression())
			# You must check value of expr to be able to cast by int().
			return expr


	def visitExpression(self, ctx):
		""" UnitXObject同士を計算した結果を返す．
			return: UnitXObject
		"""
		if ctx.expression(i=0):
			# x,y: UnitXObject
			x = self.visitExpression(ctx.expression(i=0))

			if ctx.start.type == UnitXLexer.INC: return self.calc.increment(x)
			elif ctx.start.type == UnitXLexer.DEC: return self.calc.decrement(x)
			else:
				y = self.visitExpression(ctx.expression(i=1))
				an_operator = ctx.getChild(i=1).getSymbol()
				if an_operator.type == UnitXLexer.ADD: return self.calc.add(x,y)
				elif an_operator.type == UnitXLexer.SUB: return self.calc.subtract(x,y)
				elif an_operator.type == UnitXLexer.MUL: return self.calc.multiply(x,y)
				elif an_operator.type == UnitXLexer.DIV: return self.calc.divide(x,y)
				elif an_operator.type == UnitXLexer.ASSIGN: return self.calc.assign(x,y)
				elif an_operator.type == UnitXLexer.ADD_ASSIGN: return self.calc.add_assign(x,y)
				elif an_operator.type == UnitXLexer.SUB_ASSIGN: return self.calc.substract_assign(x,y)
				elif an_operator.type == UnitXLexer.MUL_ASSIGN: return self.calc.multiply(x,y)
				elif an_operator.type == UnitXLexer.DIV_ASSIGN: return self.calc.divide(x,y)
				elif an_operator.type == UnitXLexer.MOD_ASSIGN: pass

		elif ctx.primary(): return self.visitPrimary(ctx.primary())
		else: raise Exception("Syntax error. UnitXEvalVisitor#visitExpression") # Never happen.


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
		if ctx.Identifier():
			return UnitXObject(ctx.Identifier().getText(), is_identifier=True)

		elif ctx.literal():
			a_value = self.visitLiteral(ctx.literal())
			return UnitXObject(a_value)

		elif ctx.start.type == UnitXLexer.LPAREN:
			return self.visitExpression(ctx.expression(i=0))

		elif ctx.start.type == UnitXLexer.LBRACK:
			unitx_objs = [self.visitExpression(an_expr) for an_expr in ctx.expression()]
			return UnitXObject(unitx_objs)

		else: raise Exception("Syntax error. UnitXEvalVisitor#visitPrimary") # Never happen.


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

