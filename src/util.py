#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import prettyprint
from constants import Constants

class Util(object):
    """A class which is compiled versatile utility functions."""

    @classmethod
    def dump(self, an_obj):
        """Prints a debug value without misconversion.
        
        Prints a debug value without a misconversion for UTF-8 strings 
        in a list or a dict class, because it's not supported by Python.

        Args:
            an_obj: An instance of a list or a dict class.
        """
        sys.stderr.write(prettyprint.pp_str(an_obj) + '\n')

    @classmethod
    def printf(self, is_test, called_func, content):
        """Prints a variable with some filters.
        
        Args:
            is_test: A bool whether this process is a test mode.
            called_func: An instance of Function that calls this function.
            content: A variable which is printed by this lang.
        """
        is_DEBUG = False
        if is_DEBUG: print "A method of UnitX:", type(called_func)
        if not is_test: print content
        return

    @classmethod
    def filter_to_white(self, string):
        """Filters a string line to whitespace.
        
        Args:
            string: A string of a code line.
        Returns:
            spaces: A string of whitespaces.
        """
        spaces = u''
        for char in string:
            if char == u'\t':
                spaces += u'\t'
            elif Util.is_ascii(char):
                spaces += u' '
            else:
                spaces += u'　'
        return spaces


    @classmethod
    def is_ascii(self, string):
        """Returns that whether a string of argument is ascii characters.
        
        Args:
            string: A string of unicode.
        Returns:
            A bool whether a string of argument is ascii characters.
        """
        if string:
            return max([ord(char) for char in string]) < 128
        return True


def main():
    """Run an example for a Util class."""

    Util.dump(['あ', 'い', 'う'])
    Util.dump({'title':'ねじまき鳥', 'author':'村上春樹'})

    print Util.is_ascii(u"""abc m(__)m""")
    print Util.is_ascii(u'あいうえお')

    code = u'面積\t= 距離 * 高さ'
    print "|%s|" % code
    print "|%s|" % Util.filter_to_white(code)

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
