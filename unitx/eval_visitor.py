#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import pkgutil

from antlr4 import *
from UnitXVisitor import UnitXVisitor
from UnitXParser import UnitXParser
from UnitXLexer import UnitXLexer

from unitx_object import UnitXObject
from unitx_object_calc import UnitXObjectCalc
from scope_list import ScopeList
from util import Util
from constants import Constants
from defined_function import DefinedFunction
from unit import Unit
from unit_manager import UnitManager
from mediator import Mediator
from scope import Scope

class EvalVisitor(UnitXVisitor, Mediator):
	""" UnitXの構文木をたどり，その振る舞いを行うクラス．

	UnitXParserから，このクラスにある各visit関数が呼ばれ，実行される．それぞれの構文ごとに振る舞いが行われ，それが言語としてのアウトプットとなる．
	また，このファイルを呼び出す側のUnitXParserは，Grammarファイル(UnitX.g4)のBNFを元にANTLRが生成したクラスであるため，UnitX.g4のBNFとこのクラスの関数は対応関係にある．例えば，<statement>というルールは，このクラスのvisitStatement(ctx)に対応する．

	Attributes:
		_scopes: すべてのスコープ情報が入っているリスト
		_calc: UnitXObjectの演算を行うクラスのインスタンス
	"""
	
	def __init__(self, is_intaractive_run, an_errhandler):
		""" EvalVisitorを初期化して応答する．
		"""
		#self.is_break = False
		self.is_intaractive_run = is_intaractive_run
		self.errhandler = an_errhandler
		self._scopes = ScopeList()
		self.calc = UnitXObjectCalc()

		this_dir, _ = os.path.split(__file__)
		data_path = os.path.join(this_dir, "data/unit_table.dat")
		self.unit_manager = UnitManager(data_path) # Sets a database(data/unit_table.dat) for calculating units.
		
		#
		# Sets a mediator to each classes for a management,
		# because this class is a mediator class.
		# Also, UnitXObject, Unit, Scope classes have to create many new instances.
		# So, We set a mediator by using classmethod.
		#
		self.calc.set_mediator(self)
		self._scopes.set_mediator(self)
		self.unit_manager.set_mediator(self)
		UnitXObject.set_mediator(self)
		Unit.set_mediator(self)
		Scope.set_mediator(self)


	#
	# Implementations of Mediator are below.
	# =======================================
	#
	def get_parser(self):
		return self
	
	def get_scopes(self):
		return self._scopes

	def get_errhandler(self):
		return self.errhandler
	
	def get_is_intaractive_run(self):
		return self.is_intaractive_run
	
	def get_unit_manager(self):
		return self.unit_manager

	#
	# Implementations of UnitXVisitor are below.
	# =======================================
	#
	def visitProgram(self, ctx):
		""" Just visiting child nodes of UnitX syntax.
			ALSO, THIS <program> RULE IS A STARTING POINT OF UNITX PARSER.
		"""
		return self.visitChildren(ctx)

	def visitTypeDeclaration(self, ctx):
		""" Just visiting child nodes of UnitX syntax."""
		return self.visitChildren(ctx)


	def visitFunctionDeclaration(self, ctx):
		""" 関数宣言をする．
		"""
		if self._is_ignored_block(ctx.block()): return

		func_name, func_args = ctx.Identifier().getText(), self.visitFormalParameters(ctx.formalParameters())
		current_scope = self._scopes.peek()
		def_func = DefinedFunction(func_name, func_args, ctx, current_scope)

		unitx_obj = UnitXObject(value=def_func, varname=func_name, unit=None)
		self._scopes.regist_unitx_obj(func_name, unitx_obj)
		return


	def _call_function(self, called_func_name, called_args):
		""" expressionから呼ばれる．
		"""
		found_scope = self._scopes.peek().find_scope_of(called_func_name)
		if found_scope:
			def_func = found_scope[called_func_name].get_value()

			self._scopes.new_scope()
			if called_args:
				args_without_default = [[var, unitx_obj] for var, unitx_obj in def_func.args if not unitx_obj]
				#print len(args_without_default), len(called_args)
				if len(called_args) < len(args_without_default):
					sys.stderr.write('引数足りないError') #引数足りないerror
					sys.exit(1)
				if len(called_args) > len(def_func.args):
					sys.stderr.write('引数多すぎError') #引数多すぎerror
					sys.exit(1)
				#Util.dump(def_func.args)
				for i in range(len(def_func.args)):
					varname, default_value = def_func.args[i]
					if i < len(called_args):
						unitx_obj = called_args[i]
					else:
						if not default_value:
							default_value = UnitXObject(value=None,varname=None,unit=None,is_none=True)
						unitx_obj = default_value
					self.calc.assign(UnitXObject(value=None,varname=varname,unit=None),unitx_obj)

			# TODO(Tasuku): 現在は定義した関数のみ使用可能だが，組み込み関数はまだなので，それを後で追加
			self.visitBlock(def_func.ctx.block())
			self._scopes.del_scope()
		else:
			pass # error
		
		return None # res of func


	def visitFormalParameters(self, ctx):
		"""
		"""
		if ctx.formalParameterList(): return self.visitFormalParameterList(ctx.formalParameterList())
		return None


	def visitFormalParameterList(self, ctx):
		""" 
		"""
		return [self.visitFormalParameter(a_param) for a_param in ctx.formalParameter()]


	def visitFormalParameter(self, ctx):
		"""
			 varname -- A key registing in a scope
		"""
		varname = ctx.Identifier().getText()
		if ctx.expression():
			default_value = self.visitExpression(ctx.expression())
		else:
			default_value = None

		return [varname, default_value]


	def _is_ignored_block(self, ctx):
		""" Returns whether ignored block exists for intaractive programing.
			Ignored block is like bellow.
			Example:
				$ unitx
				unitx> rep(i,5) {
				...... }
			In intaractive programing, we have to ignore runtime errors in a block statement.
			So, we control it by turning on a variable "is_ignored_block" in EvalError.
			And the controled result is turned off by a user input an empty string.
		"""
		return self.is_intaractive_run and self.errhandler.is_ignored_block


	def visitBlock(self, ctx):
		"""
		"""

		a_parent, a_grandparent = ctx.parentCtx, ctx.parentCtx.parentCtx
		is_special_block = (isinstance(a_grandparent, UnitXParser.RepStatementContext) or isinstance(a_grandparent, UnitXParser.IfStatementContext) or isinstance(a_parent, UnitXParser.FunctionDeclarationContext))

		#
		# If the block is "rep", "if", and "fucntion" statements,
		# don't create a scope in this visitBlock function because of initializing it in another function.
		# Also, the block is a "block" statement which is like a '{' .... '}', must create a scope.
		#
		if is_special_block:
			self.visitChildren(ctx)
		else:
			self._scopes.new_scope()
			self.visitChildren(ctx)
			self._scopes.del_scope()
		return 


	def visitBlockStatement(self, ctx):
		""" Just visiting child nodes of UnitX syntax."""
		return self.visitChildren(ctx)


	def visitStatement(self, ctx):
		""" それぞれの文を辿って，応答する．
		"""
		#Util.dump(self._scopes)
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
			raise Exception("Syntax error. EvalVisitor#visitStatement") # Never happen.

		return


	def visitBorderStatement(self, ctx):
		""" 線を出力して応答する(borderとして3~10個の-を使える）．
			ex: ---, ----, -----
		"""
		sys.stdout.write(ctx.start.text + '\n')
		return

	# Visit a parse tree produced by UnitXParser#repStatement.
	def visitRepStatement(self, ctx):
		""" 与えられた回数の繰り返し処理を実行し，応答する．
			また，繰り返し処理の前にスコープのメモリ領域を確保し，繰り返し処理の後にそのスコープのメモリ領域を解放する．すなわち，スコープを管理する．
			ex: rep(i,5){...}, rep(i,[1,2,3]){...}, rep(i,[{B},{KB},{MB}])
		"""
		if self._is_ignored_block(ctx.statement()): return

		var_obj, end_control = self.visitRepControl(ctx.repControl())
		end_value = end_control.get_value()
		if isinstance(end_value, int):
			repeat_list = [UnitXObject(value=x,varname=None,unit=Unit()) for x in range(end_value)]
		else:
			repeat_list = end_value
		self._scopes.new_scope()

		for unitx_obj in repeat_list:
			self.calc.assign(var_obj, unitx_obj)
			self.visitStatement(ctx.statement())

		self._scopes.del_scope()
		return


	def visitIfStatement(self, ctx):
		""" 与えられたexpressionの結果
			BNF: 'if' parExpression statement ('else' statement)?
		"""
		unitx_obj = self.visitParExpression(ctx.parExpression())
		is_run_ifStatement = unitx_obj.get_value()
		if is_run_ifStatement:
			if self._is_ignored_block(ctx.statement(i=0)): return
			self.visitStatement(ctx.statement(i=0))
		else:
			if ctx.getChildCount() > 3:
				if self._is_ignored_block(ctx.statement(i=1)): return
				self.visitStatement(ctx.statement(i=1))
			else: pass # do nothing
		return		


	def visitExpressionStatement(self, ctx):
		""" Just visiting child nodes of UnitX syntax."""
		unitx_obj = self.visitExpression(ctx.expression())
		if self.is_intaractive_run:
			print "%s%s" % (unitx_obj.get_value(), unitx_obj.unit.formal_str())
		return


	def visitReturnStatement(self, ctx):
		""" Just visiting child nodes of UnitX syntax."""
		return self.visitChildren(ctx)


	def visitPrintStatement(self, ctx):
		""" 与えられたexpressionのUnitXObjectたちを出力して，応答する．
			printモードでself._print_variablesを起動する．
		"""
		self._print_variables(ctx, 'print')
		return

	def visitDumpStatement(self, ctx):
		""" 与えられたexpressionのUnitXObjectたちを出力して，応答する．
			dumpモードでself._print_variablesを起動する．
		"""
		self._print_variables(ctx, 'dump')
		return

	def _print_variables(self, ctx, mode):
		""" 与えられたexpressionのUnitXObjectたちを出力して，応答する．
			dumpモードでは，変数名とその変数に束縛されたUnitXObjectの値を出力する．
			printモードでは，UnitXObjectの値のみを出力する．
		"""
		#print self._scopes
		unitx_strs = []
		for an_expr in ctx.expression():
			unitx_obj = self.visitExpression(an_expr)
			if unitx_obj.is_none:
				dump_line = 'None' #None
			else: 
				varname = unitx_obj.varname
				if varname and mode == 'dump':
					dump_line = "%s: %s%s" % (varname, unitx_obj.get_value(), unitx_obj.unit.formal_str())
				else:
					dump_line = "%s%s" % (unitx_obj.get_value(), unitx_obj.unit.formal_str())
			unitx_strs.append(dump_line)
		sys.stdout.write(' '.join(unitx_strs) + '\n')
		return

	def visitExpressionList(self, ctx):
		""" Just visiting child nodes of UnitX syntax."""
		return [self.visitExpression(an_expr) for an_expr in ctx.expression()]


	def visitParExpression(self, ctx):
		""" LPARENとRPARENは無視して，expressionのみを辿って，結果を応答する．
		"""
		return self.visitExpression(ctx.expression())

	def visitRepControl(self, ctx):
		""" Visit a parse tree produced by UnitXParser#repControl.
			ex: [i,5], [i,[1,2,3]]
		"""
		varname = ctx.Identifier().getText()
		return [UnitXObject(value=None, varname=varname, unit=Unit()), self.visitEndRep(ctx.endRep())]


	def visitEndRep(self, ctx):
		""" 
			It checks a value of expr to be able to cast by int().
		"""
		an_expr = self.visitExpression(ctx.expression())
		# You must check value of expr to be able to cast by int().
		return an_expr


	def visitExpression(self, ctx):
		""" UnitXObject同士を計算した結果を返す．
			return: UnitXObject
		"""
		if ctx.expression(i=0):
			x = self.visitExpression(ctx.expression(i=0)) # x,y: UnitXObject

			second_token = ctx.getChild(i=1).getSymbol().type
			if ctx.start.type == UnitXLexer.INC: unitx_obj = self.calc.increment(x)
			elif ctx.start.type == UnitXLexer.DEC: unitx_obj = self.calc.decrement(x)
			elif second_token == UnitXLexer.LPAREN:
				called_func_name, called_args = x.varname, []
				if ctx.expressionList():
					called_args = self.visitExpressionList(ctx.expressionList())
				a_value = self._call_function(called_func_name, called_args)
				unitx_obj = UnitXObject(value=a_value, varname=called_func_name, unit=Unit())
			else:
				y = self.visitExpression(ctx.expression(i=1))
				if second_token == UnitXLexer.ADD: unitx_obj = self.calc.add(x,y)
				elif second_token == UnitXLexer.SUB: unitx_obj = self.calc.subtract(x,y)
				elif second_token == UnitXLexer.MUL: unitx_obj = self.calc.multiply(x,y)
				elif second_token == UnitXLexer.DIV: unitx_obj = self.calc.divide(x,y)
				elif second_token == UnitXLexer.ASSIGN: unitx_obj = self.calc.assign(x,y)
				elif second_token == UnitXLexer.ADD_ASSIGN: unitx_obj = self.calc.add_assign(x,y)
				elif second_token == UnitXLexer.SUB_ASSIGN: unitx_obj = self.calc.substract_assign(x,y)
				elif second_token == UnitXLexer.MUL_ASSIGN: unitx_obj = self.calc.multiply(x,y)
				elif second_token == UnitXLexer.DIV_ASSIGN: unitx_obj = self.calc.divide(x,y)
				elif second_token == UnitXLexer.MOD_ASSIGN: unitx_obj = None
				else:
					unitx_obj = None
		elif ctx.primary(): unitx_obj = self.visitPrimary(ctx.primary())
		else:
			raise Exception("Syntax error. EvalVisitor#visitExpression") # Never happen.

		assert(isinstance(unitx_obj, UnitXObject))

		return unitx_obj


	def visitUnit(self, ctx):
		""" Just visiting child nodes of UnitX syntax."""
		unit = self.visitUnitSingleOrPairOperator(ctx.unitSingleOrPairOperator())
		unit.replace_tokens()
		return unit


	def visitUnitSingleOrPairOperator(self, ctx):
		"""
		"""
		if ctx.start.type == UnitXLexer.AT: return Unit()
		if ctx.unitOperator(i=1):
			unit = Unit()
			numers = self.visitUnitOperator(ctx.unitOperator(i=0))
			denoms = self.visitUnitOperator(ctx.unitOperator(i=1))
			if len(numers) == 2: unit.ex_numer, unit.numer = numers
			else: unit.numer = numers[0]
			if len(denoms) == 2: unit.ex_denom, unit.denom = denoms
			else: unit.denom = denoms[0]
			return unit
		else:
			unit = Unit()
			numers = self.visitUnitOperator(ctx.unitOperator(i=0))
			if len(numers) == 2: unit.ex_numer, unit.numer = numers
			else: unit.numer = numers[0]
			return unit


	def visitUnitOperator(self, ctx):
		"""
		"""
		if ctx.Identifier(i=1):
			return [ctx.Identifier(i=0).getText(), ctx.Identifier(i=1).getText()]
		else:
			return [ctx.Identifier(i=0).getText()]


	def visitPrimary(self, ctx):
		""" それぞれのPrimaryの値をUnitXObjectにラップして，応答する．

			Identifier: variable or function
			literal: number, string, boolean, none
			PAREN=(): expression
			BRACK=[]: list
		"""
		unit = Unit()
		if ctx.unit(): unit = self.visitUnit(ctx.unit())

		if ctx.Identifier():
			# Here: ここで変数がスコープにあるかを判定し，見つかったオブジェクトを格納する．
			varname = ctx.Identifier().getText()
			found_scope = self._scopes.peek().find_scope_of(varname)
			if found_scope:
				unitx_obj = found_scope[varname]
				if not unit.is_empty():
					unitx_obj.unit = unit
			else:
				unitx_obj = UnitXObject(value=None, varname=varname, unit=unit)

		elif ctx.literal():
			a_value = self.visitLiteral(ctx.literal())
			if a_value is None:
				unitx_obj = UnitXObject(value=None, varname=None, unit=unit, is_none=True)
			else:
				unitx_obj = UnitXObject(value=a_value, varname=None, unit=unit)

		elif ctx.start.type == UnitXLexer.LPAREN:
			unitx_obj = self.visitExpression(ctx.expression(i=0))
			if not unit.is_empty():
				unitx_obj.unit = unit

		elif ctx.start.type == UnitXLexer.LBRACK:
			unitx_objs = []
			for an_expr in ctx.expression():
				an_obj = self.visitExpression(an_expr)
				if not unit.is_empty():
					an_obj.unit = unit
				unitx_objs.append(an_obj)
			unitx_obj = UnitXObject(value = unitx_objs, varname = None, unit=unit)
		else:
			raise Exception("Syntax error. EvalVisitor#visitPrimary") # Never happen.

		assert(isinstance(unitx_obj, UnitXObject))
		return unitx_obj


	def visitLiteral(self, ctx):
		""" それぞれのリテラルごとのvisitメソッドを呼び出し，その結果の値を応答する．
		"""
		if ctx.number(): return self.visitNumber(ctx.number())
		elif ctx.string(): return self.visitString(ctx.string())
		elif ctx.boolean(): return self.visitBoolean(ctx.boolean())
		elif ctx.none(): return None
		else: raise Exception("Syntax error. EvalVisitor#visitLiteral") # Never happen.


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
		a_value = True if ctx.start.text == 'true' else False
		return a_value

