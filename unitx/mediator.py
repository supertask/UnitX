#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Mediator(object):
	""" Mediator interface for Mediator pattern.
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
