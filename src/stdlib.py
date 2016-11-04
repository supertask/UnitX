#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from constants import Constants
from collegue import Collegue
from function import BuiltInFunction

class Stdlib(Collegue):
    """A built-in(standard) library in UnitX.

    Attributes:
        funcs: A list of BuiltInFunction classes.
    """

    def __init__(self):
        """Inits attributes of a Stdlib class. """
        self.funcs = [
            BuiltInFunction('expect', [['l',None],['r',None]], self.expect)
        ]


    def expect(self, args, func_obj):
        """Checks a variable of args and reports an error.

        Args:
            args: A list of instances of UnitXObject.
            func_obj: An instance of UnitXObject indicating this function.
        Returns:
            An instance of UnitXObject which is an empty.
        Raises:
            ExpectError: An error occurred by a difference when values of
                args are not same.
        """
        l, r = args
        #リスト用の評価を書く
        is_match = l.equals(r).get_value()
        if not is_match:
            msg = Constants.EXPECT_ERR % (l.get_unit_value(), r.get_unit_value())
            self.mediator.get_parser().notifyErrorListeners(msg, func_obj.token, Exception(msg)) #Bug
            sys.exit(Constants.EXIT_FAILURE_IN_UNITX)
        return self.mediator.NULL_UNITX_OBJ


    def r(self, args, func_obj):
        """Returns a list indicated by a range of args.

        Args:
            args: A list of instances of UnitXObject.
            func_obj: An instance of UnitXObject including a function.
        Returns:
            range: A list of instances of UnitXObject.
        Raises:
            TypeError: An error occurred.....
        """
        l, r = args
        is_match = l.get_value() == r.get_value() and l.unit.equals(r.unit)
        if not is_match:
            msg = Constants.EXPECT_ERR % (l.get_unit_value(), r.get_unit_value())
            self.mediator.get_parser().notifyErrorListeners(msg, func_obj.token, Exception(msg))


    def set_mediator(self, mediator):
        """Sets a mediator for Mediator pattern of GoF.
        
        Args:
            mediator: An instance of a EvalVisitor class inherited Mediator class.
        """
        self.mediator = mediator

def main():
    """Run an example for a Stdlib class."""
    from unitx_object import UnitXObject
    from unit import Unit
    from simulator import Simulator

    s = Simulator()
    UnitXObject.manager = s.get_manager()
    UnitXObject.scopes = s.get_scopes()

    l = UnitXObject(value=1.5, varname='x', is_none=False, unit=Unit(numer=u'cm'))
    r = UnitXObject(value=1.5, varname='y', is_none=False, unit=Unit(numer=u'cm'))
    func_obj = None
    stdlib = Stdlib()
    stdlib.expect([l,r], func_obj)

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
