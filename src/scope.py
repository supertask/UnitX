#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from collegue import Collegue
from constants import Constants

class Scope(dict, Collegue):
    """A class saving instances of a UnitXObject class.

    This class is created by a ScopeList class, when a block statement 
    appeared in a running point.
    And, the running point can use instances of UnitXObject existing in this 
    class during this class is alive.

    But this class is deleted by a ScopeList class, when a block statement 
    disappeared in a running point. And then, the running point cannot use instances 
    of UnitXObject existed in this class.

    Attributes:
        parent: An instance of a parent Scope of this class.
    """

    def __init__(self, parent):
        """ Inits attributes of a Scope class. """
        self.parent = parent


    def find_scope_of(self, varname):
        """Returns an instance of a Scope class indicating varname.
        
        Returns An instance indicating varname, if it exists in this scope 
        or ancestral parent scopes.

        Args:
            varname: A string of a variable.
        Returns:
            An instance of a Scope class indicating varname.
        """
        if varname in self: return self
        else:
            if self.parent == None: return None # For finishing
            tmp = self.parent.find_scope_of(varname)
            return tmp  # Search recursively


    @classmethod
    def set_mediator(self, mediator):
        """Sets a mediator for Mediator pattern of GoF.
        
        Args:
            mediator: An instance of a EvalVisitor class inherited Mediator class.
        """
        self.mediator = mediator


def main():
    """Run an example for a Scope class."""

    from unitx_object import UnitXObject
    from unit import Unit

    grandparent = Scope(None)
    grandparent['x'] = UnitXObject(value=2, varname=None, unit=Unit())
    grandparent['z'] = UnitXObject(value=4, varname=None, unit=Unit())

    parent = Scope(grandparent)
    parent['y'] = UnitXObject(value=3, varname=None, unit=Unit())

    child = Scope(parent)

    print 'A grandparent scope instance: ', grandparent
    print 'A parent scope instance: ', parent
    print 'A child scope instance: ', child

    found_scope = child.find_scope_of('x')
    print 'A value of a "x": ', found_scope['x']
    found_scope = child.find_scope_of('y')
    print 'A value of a "y": ', found_scope['y']
    found_scope = child.find_scope_of('z')
    print 'A value of a "z": ', found_scope['z']

    print child.parent.parent

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
