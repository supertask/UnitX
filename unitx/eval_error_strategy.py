#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from UnitXParser import UnitXParser

from antlr4.Token import Token
from antlr4.IntervalSet import IntervalSet
from antlr4.atn.ATNState import ATNState
from antlr4.error.Errors import NoViableAltException
from antlr4.error.Errors import InputMismatchException
from antlr4.error.Errors import FailedPredicateException
from antlr4.error.Errors import ParseCancellationException

class EvalErrorStrategy(DefaultErrorStrategy):
	"""
	"""

	def __init__(self, is_intaractive_run):
		super(EvalErrorStrategy, self).__init__()
		self.is_intaractive_run = is_intaractive_run
		self.is_ignored_block = False
		self.default_msg = "SyntaxError: "

	def _filter_newline(self, tokens):
		res = []
		for name in tokens:
			if name == u"'\n'": res.append(u"'\\n'")
			else: res.append(name)
		return res

	def reportError(self, recognizer, e):
		""" Reports each error.

			if we've already reported an error and have not matched a token
			yet successfully, don't report any errors.
		"""
		if self.is_block(recognizer): return
		if super(EvalErrorStrategy, self).inErrorRecoveryMode(recognizer):
			return # don't report spurious errors
		super(EvalErrorStrategy, self).beginErrorCondition(recognizer)

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
		msg = self.default_msg
		msg += "no viable alternative at input " + super(EvalErrorStrategy, self).escapeWSAndQuote(input)
		recognizer.notifyErrorListeners(msg, e.offendingToken, e)
	

	def reportInputMismatch(self, recognizer, e):
		""" Reports input mismatch error.
		"""
		msg = self.default_msg
		msg += "mismatched input " + super(EvalErrorStrategy, self).getTokenErrorDisplay(e.offendingToken) \
			  + " expecting " + e.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
		recognizer.notifyErrorListeners(msg, e.offendingToken, e)


	def reportFailedPredicate(self, recognizer, e):
		""" Reports failed predicate error.
		"""
		rule_name = recognizer.ruleNames[recognizer._ctx.getRuleIndex()]
		msg = self.default_msg
		msg += "rule " + rule_name + " " + e.message
		recognizer.notifyErrorListeners(msg, e.offendingToken, e)

	def reportUnwantedToken(self, recognizer):
		""" Reports unwanted token error.
			Wrote in 3/24/2016.
		"""
		if self.is_block(recognizer): return

		if super(EvalErrorStrategy, self).inErrorRecoveryMode(recognizer):
			return
		super(EvalErrorStrategy, self).beginErrorCondition(recognizer)
		t = recognizer.getCurrentToken()
		token_name = super(EvalErrorStrategy, self).getTokenErrorDisplay(t)
		expecting = super(EvalErrorStrategy, self).getExpectedTokens(recognizer)

		msg = self.default_msg
		msg += "unexpecting " + token_name + ", expecting " \
			+ expecting.toString(self._filter_newline(recognizer.literalNames), recognizer.symbolicNames)
		recognizer.notifyErrorListeners(msg, t, None)


	def reportMatch(self, recognizer):
		""" Called by when error handling ended.
		"""
		super(EvalErrorStrategy, self).endErrorCondition(recognizer)
		self.errorRecoveryMode = self.is_ignored_block


	def reportMissingToken(self, recognizer):
		""" Reports missing token error.
		"""
		if self.is_block(recognizer): return

		if super(EvalErrorStrategy, self).inErrorRecoveryMode(recognizer):
			return
		super(EvalErrorStrategy, self).beginErrorCondition(recognizer)
		t = recognizer.getCurrentToken()
		expecting = super(EvalErrorStrategy, self).getExpectedTokens(recognizer)

		msg = self.default_msg
		msg += "missing " + expecting.toString(recognizer.literalNames, recognizer.symbolicNames) \
			  + " at " + super(EvalErrorStrategy, self).getTokenErrorDisplay(t)
		recognizer.notifyErrorListeners(msg, t, None)

	def is_block(self, recognizer):
		"""
		"""
		if isinstance(recognizer._ctx, UnitXParser.BlockContext) and self.is_intaractive_run: # ignore block

			self.is_ignored_block = self.errorRecoveryMode = True
		else:
			pass
		return self.is_ignored_block

