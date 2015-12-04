class Node:
	def __init__(self, name, value, parent):
		self.name = name
		self.value = value
		self.parent = parent
		self.children = []

	def get_value(self):
		return self.value

	def get_name(self):
		return self.name

