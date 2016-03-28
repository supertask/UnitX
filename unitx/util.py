#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import prettyprint

class Util:
	""" 汎用的なユーティリティ関数をまとめたクラス．
	"""

	@classmethod
	def dump(self, an_object):
		""" listやdictの中のutf-8文字の文字列に対して，文字化けなくデバッグ出力して応答する（Pythonの標準ではサポートされていないため）．
		"""
		sys.stderr.write(prettyprint.pp_str(an_object) + '\n')

	@classmethod
	def filter_to_white(self, a_str):
		spaces = u''
		for a_char in a_str:
			a_char
			if a_char == u'\t':
				spaces += u'\t'
			elif Util.is_ascii(a_char):
				spaces += u' '
			else:
				spaces += u'　'
		return spaces

	@classmethod
	def is_ascii(self, string):
		""" Returns true if non ascii characters are detected in the given string.
		"""
		if string:
			return max([ord(char) for char in string]) < 128
		return True

def main():
	Util.dump(['あ', 'い', 'う'])
	Util.dump({'title':'ねじまき鳥', 'author':'村上春樹'})

	print Util.is_ascii(u"""abc m(__)m""")
	print Util.is_ascii(u'あいうえお')

	code = u'面積 = 距離 * 高さ'
	print "|%s|" % code
	print "|%s|" % Util.filter_to_white(code)

	return 0

if __name__ == '__main__':
	sys.exit(main())
