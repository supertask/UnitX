class ParsingTest():
	def __init__(self):
		import sys
		#if len(sys.argv) < 2: sys.exit(1)
		a_filepath = "test/test_code_0.num" #sys.argv[1]
		self.parser = parser.MainParser(a_filepath)


	def test_constant(self):
		test_lines = 		["12.5", "1521.", ".5", "55", "99.9aaa"]
		test_res_lines =	[12.5, 1521., .5, 55, 99.9]
		for test_line, test_res_line in zip(test_lines, test_res_lines):
			self.parser.index=0
			self.parser.lines = test_line
			res = self.parser.constant()
			assert res == test_res_line
			assert type(res) == type(test_res_line)

	def test_is_wchar(self):
		test_lines = 		["", "SSFEFE", "aaa22", "22ge"]
		for test_line in test_lines:
			for a_char in test_line:
				print a_char, self.parser.is_wchar(a_char)
			print

	def test_variable(self):
		test_lines = [u'変数XXX',u'aa',u'xxxx32', u'ほげ32'] #,u'ほ+', u'++']
		test_res_lines = test_lines

		for test_line, test_res_line in zip(test_lines, test_res_lines):
			self.parser.index=0
			self.parser.lines = test_line
			res = self.parser.variable()
			print res.encode('utf-8'), test_line.encode('utf-8')
			assert res == test_res_line
			
	def test_expr(self):
		t_inputs = ['20*1.22+52','32*(52+2)','(51+(6163+5252)-52)/3', '52/52'] #,u'ほ+', u'++']
		t_anses = map(eval, t_inputs)
		self.test_template(t_inputs, t_anses, self.parser.expr)

	def test_assign(self):
		t_inputs = [u'V=20*1.22+52',u'あああ=32*(52+2)',u'あああ22=(51+(6163+5252)-52)/3', u'XX_men=52/52'] #,u'ほ+', u'++']
		t_anses = ['', '', '', ''] #map(eval, t_inputs)
		self.test_template(t_inputs, t_anses, self.parser.assign, is_debug=False, is_assert=False)
		print self.parser.dict_of_global_var

	def test_template(self, t_inputs, t_anses, t_func, is_debug=True, is_assert=True):
		for t_input, t_ans in zip(t_inputs, t_anses):
			self.parser.index=0
			self.parser.lines = t_input
			t_output = t_func()
			if is_debug: print t_output, t_ans
			if is_assert: assert t_output == t_ans
				
	def test_statements(self):
		t_inputs = [u'V=20*1.22+52\nprint V\n']
		t_anses = ['76.4'] #map(eval, t_inputs)
		self.test_template(t_inputs, t_anses, self.parser.statements, is_debug=False, is_assert=False)

	def setUp(self):
		print "Check.."

	def tearDown(self):
		print "The test was successful!"
