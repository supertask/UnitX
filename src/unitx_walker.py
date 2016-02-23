# -*- coding: utf-8 -*-
# Generated from UnitX.g4 by ANTLR 4.5.1
from antlr4 import *
from UnitXListener import UnitXListener
from UnitXParser import UnitXParser
from UnitXLexer import UnitXLexer

# This class defines a complete listener for a parse tree produced by UnitXParser.
class UnitXWalker(UnitXListener):

    def __init__(self):
		self.expr_buff = []

    # Enter a parse tree produced by UnitXParser#program.
    def enterProgram(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#program.
    def exitProgram(self, ctx):
        pass

    # Enter a parse tree produced by UnitXParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx):
        # 関数以下の木を保存しておく
        pass

    # Exit a parse tree produced by UnitXParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#formalParameters.
    def enterFormalParameters(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#formalParameters.
    def exitFormalParameters(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#formalParameterList.
    def enterFormalParameterList(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#formalParameterList.
    def exitFormalParameterList(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#formalParameter.
    def enterFormalParameter(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#formalParameter.
    def exitFormalParameter(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#statement.
    def enterStatement(self, ctx):
        if ctx.block():
            pass
            # print ctx.start.line # line number
        elif ctx.start.type == UnitXLexer.LOOP:
            pass
        elif ctx.start.type == UnitXLexer.IF:
            pass
        elif ctx.start.type == UnitXLexer.PRINT:
            pass
        elif ctx.start.type == UnitXLexer.AT:
            pass
        elif ctx.start.type == UnitXLexer.RETURN:
            pass
        elif ctx.start.type == UnitXLexer.BREAK:
            pass
        elif ctx.start.type == UnitXLexer.CONTINUE:
            pass
        elif ctx.borderPrinter():
            print ctx.start.text
        elif ctx.expression():
            pass


    # Exit a parse tree produced by UnitXParser#statement.
    def exitStatement(self, ctx):
        pass

    # Enter a parse tree produced by UnitXParser#borderPrinter.
    def enterBorderPrinter(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#borderPrinter.
    def exitBorderPrinter(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#block.
    def enterBlock(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#block.
    def exitBlock(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#blockStatement.
    def enterBlockStatement(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#blockStatement.
    def exitBlockStatement(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#expressionList.
    def enterExpressionList(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#expressionList.
    def exitExpressionList(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#parExpression.
    def enterParExpression(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#parExpression.
    def exitParExpression(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#forControl.
    def enterForControl(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#forControl.
    def exitForControl(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#endFor.
    def enterEndFor(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#endFor.
    def exitEndFor(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#collection.
    def enterCollection(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#collection.
    def exitCollection(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#expression.
    def enterExpression(self, ctx):
        if ctx.primary():
            pass
        elif ctx.expression(i=0):
            print ctx.getChild(i=1)
            if ctx.getChild(i=1) == UnitXLexer.MUL:
				expr_buff.append(expr_buff.pop() * expr_buff.pop())
            elif ctx.getChild(i=1) == UnitXLexer.DIV:
				expr_buff.append(expr_buff.pop() / expr_buff.pop())
            elif ctx.getChild(i=1) == UnitXLexer.ADD:
				expr_buff.append(expr_buff.pop() + expr_buff.pop())
            elif ctx.getChild(i=1) == UnitXLexer.SUB: 
				expr_buff.append(expr_buff.pop() - expr_buff.pop())
                

        #elif ctx.start.type == UnitXLexer.LOOP:
        """
        if ctx.getStart().getType() == UnitXParser.RULE_primary:
            pass
        elif ctx.getStart().getType() == UnitXParser.RULE_expression:
            pass
        #elif ctx.getStart() ==  INC
        """

    # Exit a parse tree produced by UnitXParser#expression.
    def exitExpression(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#unit.
    def enterUnit(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#unit.
    def exitUnit(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#unitSingleOrPairOperator.
    def enterUnitSingleOrPairOperator(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#unitSingleOrPairOperator.
    def exitUnitSingleOrPairOperator(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#unitOperator.
    def enterUnitOperator(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#unitOperator.
    def exitUnitOperator(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#primary.
    def enterPrimary(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#primary.
    def exitPrimary(self, ctx):
        pass


    # Enter a parse tree produced by UnitXParser#literal.
    def enterLiteral(self, ctx):
        pass

    # Exit a parse tree produced by UnitXParser#literal.
    def exitLiteral(self, ctx):
        pass


