#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from antlr4.error.ErrorListener import ErrorListener
from collegue import Collegue
from util import Util
from constants import Constants
import linecache
from function import DefinedFunction

class EvalErrorListener(ErrorListener, Collegue):
	"""
	"""
	
	def __init__(self, visitor):
		self.set_mediator(visitor)
		self.set_last_called_func(None)
		self._is_exit = False
	
	def set_mediator(self, mediator):
		self.mediator = mediator

	def get_code(self):
		if self.mediator.is_intaractive_run: return self.codelines
		else: return self.codepath

	def set_exit(self):
		self._is_exit = True

	def reset_exit(self):
		self._is_exit = False

	def is_exit(self):
		return self._is_exit
	
	def set_last_called_func(self, last_called_func):
		"""
		
		"""
		if isinstance(last_called_func, DefinedFunction):
			self.last_called_func = last_called_func
		else:
			self.last_called_func = None

	def trace_an_error(self, func, tracing_infos):
		"""
		"""
		if func:
			if func.ctx:
				tracing_info = {'name': func.name, 'line': func.func_obj.token.line, 'code': func.code}
				tracing_infos.insert(0,tracing_info)
			return self.trace_an_error(func.called_func, tracing_infos)
		else:
			return tracing_infos
	
	def write_traced_infos(self, row):
		filename = ''
		if self.mediator.is_intaractive_run: filename = '<stdin>'
		else: filename = self.codepath

		if self.last_called_func:
			traced_infos = self.trace_an_error(self.last_called_func, [])
		else:
			traced_infos = []
		traced_infos.insert(0, {'name': '<unitx>', 'line': None, 'code': self.get_code()})
		traced_infos.append({'name': None, 'line': row, 'code': self.get_code()})
		for i in range(len(traced_infos)-1):
			sys.stderr.write('%s: line %s in %s\n' % (filename, traced_infos[i+1]['line'], traced_infos[i]['name']))
		traced_infos.pop()

		return traced_infos

	def write_error_message(self, error_line, column, msg):
		error_line = error_line.rstrip()
		whites = list(Util.filter_to_white(error_line))
		whites[column] = '^'
		mark_line = ''.join(whites)
		sys.stderr.write(msg + '\n' + error_line + '\n' + mark_line + '\n')


	def syntaxError(self, recognizer, offendingSymbol, row, column, msg, e):
		if self.is_exit(): return
		traced_infos = self.write_traced_infos(row)

		error_line = ''
		if self.mediator.is_intaractive_run:
			error_line = traced_infos[-1]['code'][row-1]
		else:
			error_line = linecache.getline(self.codepath, row)
			linecache.clearcache() 

		self.write_error_message(error_line, column, msg)

		self.set_exit()
		if not self.mediator.is_intaractive_run:
			sys.exit(Constants.EXIT_FAILURE_IN_UNITX)

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

