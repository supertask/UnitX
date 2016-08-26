#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from unitx_object import UnitXObject
from unit_manager import UnitManager
from scope_list import ScopeList
from constants import Constants

class Simulator(object):

	def __init__(self):
		this_dir, _ = os.path.split(__file__)
		data_path = os.path.join(this_dir, Constants.SYSTEM_UNIT_DATA)
		self.manager = UnitManager(data_path)
		self.scopes = ScopeList()
		self.scopes.new_scope()
	
	def get_scopes(self):
		return self.scopes

	def get_manager(self):
		return self.manager


