# -*- coding: utf-8 -*-
from cmd import Cmd

"""
try:
	import readline
except ImportError:
	# readline モジュールがないときは無視する
	pass
else:
	import rlcompleter
	readline.parse_and_bind("tab: complete")
"""

import console_line

class UnitXCommand(Cmd):
	Cmd.prompt = "unitx> "
	Cmd.intro = console_line.get_line()

	def __init__(self):
		Cmd.__init__(self)

	def do_demo(self, arg):
		print "Demo: "

	def help_demo(self):
		print "help : hoge"

	def do_EOF(self, arg):
		print
		return True

	def emptyline(self):
		pass

if __name__ == '__main__':
	UnitXCommand().cmdloop()
