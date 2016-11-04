#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Mediator(object):
    """A mediator interface for Mediator pattern.

    A reference of the mediator pattern:
        Erich Gamma, John Vlissides, Ralph Johnson, and Richard Helm, "Design Patterns: Elements of Reusable Object-Oriented Software", Addison-Wesley, 1994
        Online book, https://books.google.com/books/about/Design_Patterns.html?id=6oHuKQe3TjQC&printsec=frontcover&source=kp_read_button#v=onepage&q&f=false
    """

    def get_parser(self):
        """Gets a parser for error handling and knowing token infomations."""
        pass
    
    def get_scopes(self):
        """Gets scopes for accessing value of variable of each scope."""
        pass

    def get_errhandler(self):
        """Gets an error handler for ignoring a block statement on intaractive mode."""
        pass
    
    def get_is_intaractive_run(self):
        """Gets whether intaractive mode."""
        pass
    
    def get_errlistener(self):
        """Gets an error listener."""
        pass
