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

def main():
	Util.dump(['あ', 'い', 'う'])
	Util.dump({'title':'ねじまき鳥', 'author':'村上春樹'})

	return 0

if __name__ == '__main__':
	sys.exit(main())
