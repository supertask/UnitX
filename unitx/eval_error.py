#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from UnitXParser import UnitXParser

from antlr4.Token import Token
from antlr4.IntervalSet import IntervalSet
from antlr4.atn.ATNState import ATNState
from antlr4.error.Errors import NoViableAltException, InputMismatchException, FailedPredicateException, ParseCancellationException

class EvalError(DefaultErrorStrategy):
	"""
	"""
	# TODO(Tasuku): インタラクティブのとき，rep() { if() {} } で不具合

	def __init__(self, is_interactive_run):
		super(EvalError, self).__init__()
		self.is_ignored_block = False
		self.is_interactive_run = is_interactive_run

	def reportError(self, recognizer, e):
		""" Reports each error.

			if we've already reported an error and have not matched a token
			yet successfully, don't report any errors.
		"""
		if self.is_block(recognizer): return

		if super(EvalError, self).inErrorRecoveryMode(recognizer):
			return # don't report spurious errors
		super(EvalError, self).beginErrorCondition(recognizer)
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
		msg = "no viable alternative at input " + super(EvalError, self).escapeWSAndQuote(input)
		recognizer.notifyErrorListeners(msg, e.offendingToken, e)
	

	def reportInputMismatch(self, recognizer, e):
		""" Reports input mismatch error.
		"""
		msg = "mismatched input " + super(EvalError, self).getTokenErrorDisplay(e.offendingToken) \
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
		if self.is_block(recognizer): return

		if super(EvalError, self).inErrorRecoveryMode(recognizer):
			return
		super(EvalError, self).beginErrorCondition(recognizer)
		t = recognizer.getCurrentToken()
		tokenName = super(EvalError, self).getTokenErrorDisplay(t)
		expecting = super(EvalError, self).getExpectedTokens(recognizer)
		msg = "extraneous input " + tokenName + " expecting " \
			+ expecting.toString(recognizer.literalNames, recognizer.symbolicNames)
		recognizer.notifyErrorListeners(msg, t, None)


	def reportMatch(self, recognizer):
		""" Called by when error handling ended.
		"""
		super(EvalError, self).endErrorCondition(recognizer)
		self.errorRecoveryMode = self.is_ignored_block


	def reportMissingToken(self, recognizer):
		""" Reports missing token error.
		"""
		if self.is_block(recognizer): return

		if super(EvalError, self).inErrorRecoveryMode(recognizer):
			return
		super(EvalError, self).beginErrorCondition(recognizer)
		t = recognizer.getCurrentToken()
		expecting = super(EvalError, self).getExpectedTokens(recognizer)

		msg = "missing " + expecting.toString(recognizer.literalNames, recognizer.symbolicNames) \
			  + " at " + super(EvalError, self).getTokenErrorDisplay(t)
		recognizer.notifyErrorListeners(msg, t, None)


	def is_block(self, recognizer):
		if isinstance(recognizer._ctx, UnitXParser.BlockContext) and self.is_interactive_run: # ignore block
			self.is_ignored_block = self.errorRecoveryMode = True
			return True
		return False
