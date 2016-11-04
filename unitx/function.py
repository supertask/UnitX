#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from constants import Constants
from collegue import Collegue
from unitx_object import UnitXObject
from unit import Unit
from util import Util

class Function(Collegue):
    """A class saving an infomation of a function.
    
    Attributes:
        name: A string indicating function name.
        defined_args: A list of string indicating function argument.
        ctx: An instance of ParserRuleContext indicating functionDeclaration RULE.
        func_p: An instance indicating an address of a built-in function in python.
        code: A string indicating a source code (an intaractive code or an IO path).
    """

    def __init__(self, name, defined_args, ctx=None, func_p=None, code=None):
        """Inits attributes of a Function class. """
        self.name = name
        self.defined_args = defined_args
        self.ctx = ctx
        self.func_p = func_p
        self.func_obj = None
        self.called_func = None
        self.code = code

    def call(self, args, func_obj, called_func):
        """Call a defined function with called arguments.

        This function is actually an abstract function.
        So, it needs to implement on the super class.

        Args:
            args: A list of a argument appointed/called by user.
            func_obj: An instance of UnitXObject including a function name.
            called_func: An instantce of Function which called this function.
                This a variable is used to trace an error on the EvalErrorListener.
        Returns:
            An instance of UnitXObject calculated by this function.
        """
        self.func_obj = func_obj
        self.called_func = called_func
        self.check_arguments(args, func_obj, called_func)
        return None


    def check_arguments(self, args, func_obj, called_func):
        """Checks arguments of the Function.
        
        Checks that arguments of this function are not enougn or too much.
        When it's found, it's raised an error againt an EvalErrorListener class.
        
        Args:
            args: A list of a argument appointed/called by user.
            func_obj: An instance of UnitXObject including a function name.
            called_func: An instantce of Function which called this function.
                This a variable is used to trace an error on the EvalErrorListener.
        """
        # variable, default_value: UnitXObject
        args_without_default = []
        for variable, default_value in self.defined_args:
            if not default_value:
                args_without_default.append([variable, None])

        #
        # An error which arguments are not enougn.
        #
        if len(args) < len(args_without_default):
            msg = Constants.TYPE_ERR_ARGS % (self.name, len(args_without_default), len(args))
            if args: 
                last_unitx_obj = args[-1]
                self.mediator.get_parser().notifyErrorListeners(msg, last_unitx_obj.token, Exception(msg))
            else: 
                self.mediator.get_parser().notifyErrorListeners(msg, self.ctx.start, Exception(msg))

        #
        # An error which arguments are too much.
        #
        if len(args) > len(self.defined_args):
            msg = Constants.TYPE_ERR_ARGS % (self.name, len(self.defined_args), len(args))
            last_unitx_obj = args[-1]
            self.mediator.get_parser().notifyErrorListeners(msg, last_unitx_obj.token, Exception(msg))

        return


    def __unicode__(self):
        """Returns a string of attributes.

        Returns:
            A string of infomations of attributes.
        """
        res = "<%s: %s(%s) ctx=%s func_p=%s>" % (self.__class__.__name__, self.name, self.defined_args, self.ctx, self.func_p)
        return res

    def __str__(self):
        """Returns an encoded string of attributes.

        Returns:
            An encoded string of attributes.
        """
        return unicode(self).encode('utf-8')

    def __repr__(self):
        """Returns a string of attributes.

        Returns:
            A string of a result of a __str__() function.
        """
        return self.__str__()

    @classmethod
    def set_mediator(self, mediator):
        """Sets a mediator for Mediator pattern of GoF.
        
        Args:
            mediator: An instance of a EvalVisitor class inherited Mediator class.
        """
        self.mediator = mediator



class DefinedFunction(Function):
    """A class saving an infomation of a defined function.
    
    Attributes:
        name: A string indicating function name.
        defined_args: A list of string indicating function arguments.
        ctx: An instance of ParserRuleContext indicating functionDeclaration RULE.
        code: A string indicating a source code (an intaractive code or an IO path).
    """

    def __init__(self, name, defined_args, ctx, code):
        """Inits attributes of a Function class. """
        super(DefinedFunction, self).__init__(name, defined_args, ctx=ctx, code=code)
    

    def call(self, args, func_obj, called_func):
        """Call a defined function with called arguments.

        This function is actually an abstract function.
        So, it needs to implement on the super class.

        Args:
            args: A list of a argument appointed/called by user.
            func_obj: An instance of UnitXObject including a function name.
            called_func: An instantce of Function which called this function.
                This a variable is used to trace an error on the EvalErrorListener.
        Returns:
            An instance of UnitXObject calculated by this function.
        """
        super(DefinedFunction, self).call(args, func_obj, called_func)
        self.define_arguments(args)
        self.mediator.visitBlock(self.ctx.block())
        return self.mediator.return_value

    def define_arguments(self, args):
        """Defines arguments of a Function class and assigns given values
        by user program into the arguments.

        Args:
            args: A list of a argument appointed/called by user.
        """
        for i in range(len(self.defined_args)):
            variable, default_value = self.defined_args[i]
            if i < len(args):
                unitx_obj = args[i]
            else:
                if default_value:
                    unitx_obj = default_value
                else:
                    unitx_obj = UnitXObject(value=None, varname=None, unit=Unit(), token=None, is_none=True)
            variable.assign(unitx_obj, None) #スコープに代入される



class BuiltInFunction(Function):
    """A class saving an infomation of a built-in function.
    
    Attributes:
        name: A string indicating function name.
        defined_args: A list of string indicating function arguments.
        func_p: An instance indicating an address of a built-in function in python.
    """

    def __init__(self, name, defined_args, func_p):
        """Inits attributes of a Function class. """
        super(BuiltInFunction, self).__init__(name, defined_args, func_p=func_p)
    

    def call(self, args, func_obj, called_func):
        """Call a defined function with called arguments.

        This function is actually an abstract function.
        So, it needs to implement on the super class.

        Args:
            args: A list of a argument appointed/called by user.
            func_obj: An instance of UnitXObject including a function name.
            called_func: An instantce of Function which called this function.
                This a variable is used to trace an error on the EvalErrorListener.
        Returns:
            An instance of UnitXObject calculated by this function.
        """
        super(BuiltInFunction, self).call(args, func_obj, called_func)
        a_value = self.func_p(args, func_obj)
        if a_value:
            return UnitXObject(value=a_value, varname=None, is_none=False, unit=Unit(), token=func_obj.token)
        else:
            return UnitXObject(value=None, varname=None, is_none=True, unit=Unit(), token=func_obj.token)


def main():
    """Run an example for a Function class."""
    from simulator import Simulator
    s = Simulator()

    # Define variables
    current_scope = s.get_scopes().peek()
    x, y = UnitXObject(None,None,None,is_none=True), UnitXObject(None,None,None,is_none=True)
    current_scope['x'] = x
    current_scope['y'] = y
    current_scope['dfs'] = DefinedFunction('dfs', [['x', x], ['y', y], ['level', None]], ctx=None, code=None)

    # Output
    from util import Util
    Util.dump(s.get_scopes())
    s.get_scopes().del_scope()

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
