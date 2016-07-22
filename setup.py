#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import unitx
from setuptools import setup

TARGET = os.path.join('bin','unitx')
sys.path.append('./tests')

with open('./README.md','r') as rf:
	README = rf.read()

setup(
	name='UnitX',
	packages=['unitx'],
	include_package_data=True,
	package_data={'unitx': ['data/*.dat']},
	version=unitx.__version__,
	description='UnitX is a script launguage.',
	long_description=README,
	url='http://github.com/0ED/unitx',
	author='Tasuku Takahashi',
	author_email='lightfox.task@gmail.com',
	license='MIT',
	scripts=[TARGET],
	install_requires=[
		'antlr4-python2-runtime'
	],
	test_suite = "tester.Tester"
)
