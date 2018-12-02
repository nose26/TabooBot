#This is just a wrapper because Java broke me, and I couldn't figure
#out another way to share this kind of date between funcions.
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