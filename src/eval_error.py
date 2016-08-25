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
		if (isinstance(recognizer._ctx, UnitXParser.BlockContext) or
			isinstance(recognizer._ctx, UnitXParser.StringContext) or
			isinstance(recognizer._ctx, UnitXParser.CommentContext)) and self.is_intaractive_run: # ignore block

			self.is_ignored_block = self.errorRecoveryMode = True
		return self.is_ignored_block




from antlr4.error.ErrorListener import ErrorListener
from collegue import Collegue
from util import Util

class EvalErrorListener(ErrorListener, Collegue):
	def __init__(self, visitor):
		self.set_mediator(visitor)
		self.set_forced_errobj(None)
		self._is_exit = False
	
	def set_mediator(self, mediator):
		self.mediator = mediator

	def get_code(self):
		if self.mediator.is_intaractive_run: return self.codelines
		else: return self.codepath

	def set_codelines(self, lines):
		self.codelines = lines

	def set_codepath(self, a_path):
		self.codepath = a_path
	
	def reset_exit(self):
		self._is_exit = False

	def is_exit(self):
		return self._is_exit
	
	def set_forced_errobj(self, unitx_obj):
		"""エラーを起こしたシンボルを別のシンボルへと強制的に変更する．
		
		インタラクティブモードで関数が呼ばれる際，エラーをトレースするのが大変なので，
		妥協策として，エラーした場所を強制書き換えする．
		"""
		self.forced_errobj = unitx_obj


	def trace_tokens(self, func, tracing_tokens):
		"""
		"""
		if func:
			if func.ctx:
				token_info = {'name': func.name, 'line': func.func_obj.token.line, 'code': func.code}
				tracing_tokens.insert(0,token_info) #token?
			return self.trace_tokens(func.called_func, tracing_tokens)
		else:
			return tracing_tokens


	def syntaxError(self, recognizer, offendingSymbol, row, column, msg, e):
		# TODO(Tasuku): 対話型のときのエラー描画のバグ
		if self.is_exit(): return

		import linecache
		target_line = ''
		filename = ''
		if self.mediator.is_intaractive_run:
			filename = '<stdin>'
			err_func = self.forced_errobj.get_value()
			traced_tokens = self.trace_tokens(err_func, [])
			traced_tokens.insert(0, {'name': '<unitx>', 'line': None, 'code': self.codelines})
			traced_tokens.append({'name': None, 'line': row, 'code':self.codelines})

			for i in range(len(traced_tokens)-1):
				print 'line %s in %s' % (traced_tokens[i+1]['line'], traced_tokens[i]['name'])

			traced_tokens.pop()
			print traced_tokens[-1]['code']
			target_line = traced_tokens[-1]['code'][row-1]
		else:
			filename = self.codepath
			target_line = linecache.getline(self.codepath, row)
		target_line = target_line.rstrip()
		whites = list(Util.filter_to_white(target_line))

		whites[column] = '^'
		mark_line = ''.join(whites)
		error_line = ""
		error_line += '%s: line %s: %s\n' % (filename, row, msg)
		error_line += target_line + '\n' + mark_line + '\n'
		sys.stderr.write(error_line)

		linecache.clearcache() 
		self._is_exit = True
		if not self.mediator.is_intaractive_run:
			sys.exit(1)

		return


