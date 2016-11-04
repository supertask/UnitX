#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
from unitx_object import UnitXObject
from unit_manager import UnitManager
from scope_list import ScopeList
from constants import Constants

class Simulator(object):
    """A class simulating a scope and a manager.
    
    Attributes:
        __scopes: An instance indicating a ScopeList class (a list structure).
        __manager: An instance indicating a UnitManager class.
    """

    def __init__(self):
        """Inits and sets a unit manager and a scope list."""
        this_dir, _ = os.path.split(__file__)
        data_path = os.path.join(this_dir, Constants.SYSTEM_UNIT_DATA)
        self.__manager = UnitManager(data_path)
        self.__scopes = ScopeList()
    
    def get_scopes(self):
        """Returns scopes for saving variables.

        Returns:
            An instance indicating a ScopeList class (a list structure).
        """
        return self.__scopes

    def get_manager(self):
        """Returns a unit manager.

        Returns:
            An instance indicating a UnitManager class.
        """
        return self.__manager


def main():
    """Run an example for a Unit class."""
    from simulator import Simulator
    s = Simulator()
    print s.get_scopes()
    s.get_scopes().del_scope()
    print s.get_scopes()


if __name__ == '__main__':
    sys.exit(main())
