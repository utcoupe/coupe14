# -*- coding: utf-8 -*-

class Goal:
	FINISHED_THRESHOLD = 50

	def __init__(self, name='Abstract', type, location=[0,0], executions=[]):
		self.__name			= name
		self.__type			= type
		self.__location 	= location
		self.executions 	= executions
		self.__finished		= 0 # From 0 (not finished) to 100 (finished)

	def updateScore(self):
		if self.isFinished():
			self.score = float("inf")
		else:
			self.score = float(self.__distance / (self.__priority * self.__points))
		return self.score

	def incrementFinished(self, by_value):
		self.__finished += int(by_value)

	def getName(self):
		return self.__name

	def isFinished(self):
		if (self.__finished > self.FINISHED_THRESHOLD):
			True
		else:
			False

	def toXml(self):
		string =  "<goal name='" + self.__name + "'>\n\t<type>" + self.__type + "</type>\n"
		string += "\t<finished>" + str(self.__finished) + "</finished>\n\t<executions>"
		for execution in self.__executions:
			string += "\n\t\t<execution>" + execution + "</execution>"
		string += "\n\t</executions>\n</goal>\n"
		return string
