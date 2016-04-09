#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import unitx
from setuptools import setup

TARGET = os.path.join('bin','unitx')
sys.path.append('./test')

with open('./README.md','r') as rf:
	readme = rf.read()

setup(
	name='UnitX',
	packages=['unitx'],
	include_package_data=True,
	package_data={'unitx': ['data/*.dat']},
	version=unitx.__version__,
	description='UnitX is a script launguage.',
	long_description=readme,
	url='http://github.com/0ED/unitx',
	author='Tasuku Takahashi',
	author_email='lightfox.task@gmail.com',
	license='MIT',
	scripts=[TARGET],
	test_suite = "totality_test.test",
	install_requires=[
		'antlr4-python2-runtime',
		'prettyprint'
	]
)
