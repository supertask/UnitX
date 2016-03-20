#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from UnitXParser import UnitXParser

from antlr4.Token import Token
from antlr4.IntervalSet import IntervalSet
from antlr4.atn.ATNState import ATNState
from antlr4.error.Errors import NoViableAltException, InputMismatchException, FailedPredicateException, ParseCancellationException

class UnitXErrorStrategy(DefaultErrorStrategy):
	"""
	"""
	# TODO(Tasuku): 関数(function)を実行するとき，実行時にしかis_ignore_blockが解除されない問題を解決する．

	def __init__(self, is_interactive_run):
		super(UnitXErrorStrategy, self).__init__()
		self.is_ignore_block = False
		self.is_interactive_run = is_interactive_run

	def reportError(self, recognizer, e):
		""" Reports each error.

			if we've already reported an error and have not matched a token
			yet successfully, don't report any errors.
		"""
		#print 'reportError', type(recognizer._ctx)
		if isinstance(recognizer._ctx, UnitXParser.BlockContext) and self.is_interactive_run: # ignore block
			self.is_ignore_block = self.errorRecoveryMode = True
			return

		if super(UnitXErrorStrategy, self).inErrorRecoveryMode(recognizer):
			return # don't report spurious errors
		super(UnitXErrorStrategy, self).beginErrorCondition(recognizer)
		if isinstance( e, NoViableAltException ):
			self.reportNoViableAlternative(recognizer, e)
		elif isinstance( e, InputMismatchException ):
			self.reportInputMismatch(recognizer, e)
		elif isinstance( e, FailedPredicateException ):
			self.reportFailedPredicate(recognizer, e)
		else:
			print("unknown recognition error type: " + type(e).__name__)
			recognizer.notifyErrorListeners(e.getOffendingToken(), e.getMessage(), e)


	def reportNoViableAlternative(self, recognizer, e):
		""" Reports no vaiable alternative error.
		"""
		tokens = recognizer.getTokenStream()
		if tokens is not None:
			if e.startToken.type==Token.EOF:
				input = "<EOF>"
			else:
				input = tokens.getText((e.startToken, e.offendingToken))
		else:
			input = "<unknown input>"
		msg = "no viable alternative at input " + super(UnitXErrorStrategy, self).escapeWSAndQuote(input)
		recognizer.notifyErrorListeners(msg, e.offendingToken, e)
	

	def reportInputMismatch(self, recognizer, e):
		""" Reports input mismatch error.
		"""
		msg = "mismatched input " + super(UnitXErrorStrategy, self).getTokenErrorDisplay(e.offendingToken) \
			  + " expecting " + e.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
		recognizer.notifyErrorListeners(msg, e.offendingToken, e)


	def reportFailedPredicate(self, recognizer, e):
		""" Reports failed predicate error.
		"""
		ruleName = recognizer.ruleNames[recognizer._ctx.getRuleIndex()]
		msg = "rule " + ruleName + " " + e.message
		recognizer.notifyErrorListeners(msg, e.offendingToken, e)



	def reportUnwantedToken(self, recognizer):
		""" Reports unwanted token error.
		"""
		if super(UnitXErrorStrategy, self).inErrorRecoveryMode(recognizer):
			return

		#print 'reportUnwantedToken', type(recognizer._ctx)
		if isinstance(recognizer._ctx, UnitXParser.BlockContext) and self.is_interactive_run: # ignore block
			self.is_ignore_block = self.errorRecoveryMode = True
			return

		super(UnitXErrorStrategy, self).beginErrorCondition(recognizer)
		t = recognizer.getCurrentToken()
		tokenName = super(UnitXErrorStrategy, self).getTokenErrorDisplay(t)
		expecting = super(UnitXErrorStrategy, self).getExpectedTokens(recognizer)
		msg = "extraneous input " + tokenName + " expecting " \
			+ expecting.toString(recognizer.literalNames, recognizer.symbolicNames)
		recognizer.notifyErrorListeners(msg, t, None)


	def reportMatch(self, recognizer):
		""" Called by when error handling ended.
		"""
		#print 'reportMatch', type(recognizer._ctx)
		super(UnitXErrorStrategy, self).endErrorCondition(recognizer)
		self.errorRecoveryMode = self.is_ignore_block


	def reportMissingToken(self, recognizer):
		""" Reports missing token error.
		"""
		if super(UnitXErrorStrategy, self).inErrorRecoveryMode(recognizer):
			return
		#print 'reportMissingToken', type(recognizer._ctx)
		if isinstance(recognizer._ctx, UnitXParser.BlockContext) and self.is_interactive_run: # ignore block
			self.is_ignore_block = self.errorRecoveryMode = True
			return
		super(UnitXErrorStrategy, self).beginErrorCondition(recognizer)
		t = recognizer.getCurrentToken()
		expecting = super(UnitXErrorStrategy, self).getExpectedTokens(recognizer)

		msg = "missing " + expecting.toString(recognizer.literalNames, recognizer.symbolicNames) \
			  + " at " + super(UnitXErrorStrategy, self).getTokenErrorDisplay(t)
		recognizer.notifyErrorListeners(msg, t, None)


