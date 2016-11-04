#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
from collegue import Collegue
from util import Util
from constants import Constants

class UnitManager(Collegue):
    """A class parsing/saving unit informations from databases
    

    Examples:
        prepare
            from fractions import Fraction as Fra
            from unitlib import UnitLib
            ul = UnitLib()
        end
        tokens
            sec minute hour day month year -> {u'sec': 1, u'minute': Fra(60), u'hour': Fra(60*60), u'day': Fra(60*60*24), u'month': Fra(60*60*24*30), u'year': Fra(60*60*24*365)}
            pm nm μm mm cm m km -> {u'pm': Fra(1), u'nm': Fra(1000), u'nm': Fra(1000**2),  u'μm': Fra(1000**3),  u'mm': Fra(1000**4), u'cm': Fra((1000**4)*10),  u'm': Fra(1000**5),  u'km': Fra(1000**6)}    
        end

    Attributes:
        filename: A string indicating a file name to parse.
        encoding: A string indicating encode for parsing a file of unit infos.
        exec_str_preparing: A string executing on the python for preparing unit libraries.
        unit_dict:
        unit_evals:
        __unit_id_dict:
        __is_updated:
    """

    def __init__(self, filename):
        """Inits attributes of a Unit class."""
        self.filename = filename
        self.encoding = 'utf-8'
        self.exec_str_preparing = ""
        self.unit_dict = {}
        self.unit_evals = []
        self.__unit_id_dict = {}
        self.__is_updated = []
        self.__parse(self.filename)

    def __parse(self, filename):
        """
            'prepare' <string> 'end'
        """
        with codecs.open(filename, 'r', encoding=self.encoding) as rf:
            line = rf.readline()
            while line:
                line = line.lstrip().rstrip()
                if line == 'prepare': self.__prepare_parsing(rf)
                elif line == 'tokens': self.__parse_tokens(rf)
                else: pass
                line = rf.readline()

    def __parse_tokens(self, rf):
        """
        """
        unit_id = 0
        line = rf.readline()
        while line:
            line = line.lstrip().rstrip()
            if line == 'end': return
            if line:
                token_line, dict_line = line.split('->')
                token_line = token_line.strip()
                dict_line = dict_line.strip()
                tokens = token_line.split()
                for a_token in tokens:
                    self.__unit_id_dict[a_token] = unit_id
                self.unit_evals.append(dict_line)
                self.__is_updated.append(False)
                unit_id += 1
            line = rf.readline()
        return


    def __prepare_parsing(self, rf):
        """
        """
        line = rf.readline()
        self.exec_str_preparing = ""
        while line:
            line = line.rstrip()
            if line == 'end':
                exec(self.exec_str_preparing, globals())
                return
            self.exec_str_preparing += line+'\n'
            line = rf.readline()
        return


    def get_exec_str_preparing(self):
        return self.exec_str_preparing


    def __update_dict(self, unit_str, unit):
        """
        """
        unit_id = self.get_unit_id(unit_str, unit)
        if self.__is_updated[unit_id]:
            return
        adding_dict = eval(self.unit_evals[unit_id])
        if isinstance(adding_dict, dict):
            self.unit_dict.update(adding_dict)
            self.__is_updated[unit_id] = True
        return
        

    def get_criterion(self, unit_str, unit):
        """
        """
        self.__update_dict(unit_str, unit)
        return self.unit_dict[unit_str]


    def get_unit_id(self, unit_str, unit):
        """
        """
        if unit_str in self.__unit_id_dict:
            return self.__unit_id_dict[unit_str]
        else:
            msg = Constants.NAME_ERR % unit_str
            self.mediator.get_parser().notifyErrorListeners(msg, unit.token, Exception(msg))


    def set_mediator(self, mediator):
        """Sets a mediator for Mediator pattern of GoF.
        
        Args:
            mediator: An instance of a EvalVisitor class inherited Mediator class.
        """
        self.mediator = mediator

def main():
    """Run an example for a Unit class."""

    from simulator import Simulator
    s = Simulator()
    manager = s.get_manager()

    minute = manager.get_criterion(u'分')
    hour = manager.get_criterion(u'時')
    value = 120 * (hour / minute)
    
    Util.dump(manager.unit_dict)
    print u'kind of unit:', manager.get_unit_id(u'分')
    print '%s分' % value
    print '-' * 10

    from unit import Unit
    print manager._trans_original_value(u"10:00 - 17:00", Unit(u'US_Eastern', u'Asia_Tokyo'))

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
