#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from antlr4.error.ErrorListener import ErrorListener
from collegue import Collegue
from util import Util
import linecache

class EvalErrorListener(ErrorListener, Collegue):
	"""
	"""
	
	def __init__(self, visitor):
		self.set_mediator(visitor)
		self.set_last_called_funcobj(None)
		self._is_exit = False
	
	def set_mediator(self, mediator):
		self.mediator = mediator

	def get_code(self):
		if self.mediator.is_intaractive_run: return self.codelines
		else: return self.codepath

	def reset_exit(self):
		self._is_exit = False

	def is_exit(self):
		return self._is_exit
	
	def set_last_called_funcobj(self, unitx_obj):
		"""エラーを起こしたシンボルを別のシンボルへと強制的に変更する．
		
		"""
		self.last_called_funcobj = unitx_obj

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
		if self.is_exit(): return

		target_line = ''
		filename = ''

		if self.mediator.is_intaractive_run:
			filename = '<stdin>'
		else:
			filename = self.codepath

		last_called_func = self.last_called_funcobj.get_value()
		traced_tokens = self.trace_tokens(last_called_func, [])
		traced_tokens.insert(0, {'name': '<unitx>', 'line': None, 'code': self.get_code()})
		traced_tokens.append({'name': None, 'line': row, 'code': self.get_code()})
		for i in range(len(traced_tokens)-1):
			sys.stderr.write('%s: line %s in %s\n' % (filename, traced_tokens[i+1]['line'], traced_tokens[i]['name']))
		traced_tokens.pop()

		if self.mediator.is_intaractive_run:
			target_line = traced_tokens[-1]['code'][row-1]
		else:
			target_line = linecache.getline(self.codepath, row)
		target_line = target_line.rstrip()
		whites = list(Util.filter_to_white(target_line))
		whites[column] = '^'
		mark_line = ''.join(whites)
		sys.stderr.write(msg + '\n' + target_line + '\n' + mark_line + '\n')

		linecache.clearcache() 
		self._is_exit = True
		if not self.mediator.is_intaractive_run:
			sys.exit(1)

		return



class EvalErrorIOListener(EvalErrorListener):
	"""
	"""
	def set_codepath(self, a_path):
		self.codepath = a_path


class EvalErrorIntaractiveListener(EvalErrorListener):
	"""
	"""
	def set_codelines(self, lines):
		self.codelines = lines

