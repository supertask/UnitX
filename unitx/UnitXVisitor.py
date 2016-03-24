# Generated from UnitX.g4 by ANTLR 4.5.1
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by UnitXParser.

class UnitXVisitor(ParseTreeVisitor):

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


    # Visit a parse tree produced by UnitXParser#block.
    def visitBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#blockStatement.
    def visitBlockStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#repStatement.
    def visitRepStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#ifStatement.
    def visitIfStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#expressionStatement.
    def visitExpressionStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#returnStatement.
    def visitReturnStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#printStatement.
    def visitPrintStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#dumpStatement.
    def visitDumpStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#borderStatement.
    def visitBorderStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#expressionList.
    def visitExpressionList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#parExpression.
    def visitParExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#repControl.
    def visitRepControl(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#endRep.
    def visitEndRep(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#expression.
    def visitExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#unit.
    def visitUnit(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#unitSingleOrPairOperator.
    def visitUnitSingleOrPairOperator(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#unitOperator.
    def visitUnitOperator(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#primary.
    def visitPrimary(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#literal.
    def visitLiteral(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#string.
    def visitString(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#number.
    def visitNumber(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#integer.
    def visitInteger(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#boolean.
    def visitBoolean(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UnitXParser#none.
    def visitNone(self, ctx):
        return self.visitChildren(ctx)


