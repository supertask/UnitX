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
    
    def get_code(self):
        pass

    def get_stdin_name(self):
        pass
    
    def set_last_called_func(self, last_called_func):
        """
        """
        if isinstance(last_called_func, DefinedFunction):
            self.last_called_func = last_called_func
        else:
            self.last_called_func = None

    def trace_the_error(self, func, tracing_infos):
        """
        """
        if func:
            if func.ctx:
                tracing_info = {'name': func.name, 'line': func.func_obj.token.line, 'code': func.code}
                tracing_infos.insert(0,tracing_info)
            return self.trace_the_error(func.called_func, tracing_infos)
        else:
            return tracing_infos
    
    def write_traced_infos(self, row):
        """
        """
        if self.last_called_func:
            traced_infos = self.trace_the_error(self.last_called_func, [])
        else:
            traced_infos = []
        traced_infos.insert(0, {'name': '<unitx>', 'line': None, 'code': self.get_code()})
        traced_infos.append({'name': None, 'line': row, 'code': self.get_code()})
        for i in range(len(traced_infos)-1):
            sys.stderr.write('%s: line %s in %s\n' % (self.get_stdin_name(), traced_infos[i+1]['line'], traced_infos[i]['name']))
        traced_infos.pop()

        return traced_infos

    def write_errmsg(self, error_line, column, msg):
        """
        """
        error_line = error_line.rstrip()
        whites = list(Util.filter_to_white(error_line))
        whites[column] = '^'
        mark_line = ''.join(whites)
        sys.stderr.write(msg + '\n' + error_line + '\n' + mark_line + '\n')

    def set_mediator(self, mediator):
        self.mediator = mediator



class EvalErrorIOListener(EvalErrorListener):
    """
    """
    def __init__(self, visitor):
        super(EvalErrorIOListener, self).__init__(visitor)

    def set_codepath(self, a_path):
        self.codepath = a_path

    def get_code(self):
        return self.codepath
    
    def get_stdin_name(self):
        return self.codepath

    def syntaxError(self, recognizer, offendingSymbol, row, column, msg, e):
        traced_infos = self.write_traced_infos(row)
        error_line = linecache.getline(self.codepath, row)
        linecache.clearcache() 
        self.write_errmsg(error_line, column, msg)
        sys.exit(Constants.EXIT_FAILURE_IN_UNITX)
        


class EvalErrorIntaractiveListener(EvalErrorListener):
    """
    """
    def __init__(self, visitor):
        super(EvalErrorIntaractiveListener, self).__init__(visitor)
        self._is_exit = False

    def set_codelines(self, lines):
        self.codelines = lines

    def get_code(self):
        return self.codelines

    def get_stdin_name(self):
        return '<stdin>'

    def syntaxError(self, recognizer, offendingSymbol, row, column, msg, e):
        if self.is_exit(): return
        traced_infos = self.write_traced_infos(row)
        error_line = traced_infos[-1]['code'][row-1]
        self.write_errmsg(error_line, column, msg)
        self.set_exit()

    def set_exit(self):
        self._is_exit = True

    def reset_exit(self):
        self._is_exit = False

    def is_exit(self):
        return self._is_exit


class EvalErrorStringCodeListener(EvalErrorListener):
    """
    """
    def __init__(self, visitor):
        super(EvalErrorStringCodeListener, self).__init__(visitor)

    def set_codelines(self, lines):
        self.codelines = lines

    def get_code(self):
        return self.codelines
    
    def get_stdin_name(self):
        return '<tmp.unit>'

    def syntaxError(self, recognizer, offendingSymbol, row, column, msg, e):
        traced_infos = self.write_traced_infos(row)
        error_line = traced_infos[-1]['code'][row-1]
        self.write_errmsg(error_line, column, msg)
        sys.exit(Constants.EXIT_FAILURE_IN_UNITX)

