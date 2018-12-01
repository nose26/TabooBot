import re
class tabooWordClass:
	currentTaboo = ""
	def __init__ (self, tabooInit):
		self.currentTaboo = tabooInit

	def getWord (self):
		return re.compile(r'(\W|^)' + self.currentTaboo + '(\W|$)')

	def setWord (self, newWord):
		self.currentTaboo = newWord

	def getRawWord (self):
		return self.currentTaboo