#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" LOGO memo
             ______           
   ____     /      \_         
  /    \——-|         \        
 /                    \       
 |                    |       
 |_                    \      
  |________            /      
      ____|           /       
     /           /\__/        
    /      __    |            
    |     /  \_   \__________ 
    |    |     \             | 
    |____|      |____________|
   __  __        _  __  _  __
  / / / /____   (_)/ /_| |/ /
 / / / // __ \ / // __/|   / 
/ /_/ // / / // // /_ /   |  
\____//_/ /_//_/ \__//_/|_|
"""

def get_line():
	"""
		Use a command for generating LOGO:
			$ figlet -kw 120 -f slant UnitX
			$ jp2a -i --width=30 --chars=" XY" --output=sample.txt unit.jpg
	"""
	import time
	now_time = time.ctime(time.time())
	ascii_art = """\
   __  __        _  __  _  __
  / / / /____   (_)/ /_| |/ /
 / / / // __ \ / // __/|   / 
/ /_/ // / / // // /_ /   |  
\____//_/ /_//_/ \__//_/|_|
"""
	unitx_info = """\
UnitX 0.7.0 (%s)
Type "help" or "demo <number(0-2)>" for UnitX life.""" % (now_time)
	console_info = ascii_art + unitx_info

	return console_info


if __name__ == '__main__':
	print get_line()
