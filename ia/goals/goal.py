# -*- coding: utf-8 -*-
from .goalExecution import GoalExecution

class Goal:
	FINISHED_THRESHOLD = 50

	def __init__(self, name, type, location, executions):
		self.__name			= str(name)
		self.__type			= str(type)
		self.__location 	= location
		self.executions 	= executions
		self.__finished		= 0 # From 0 (not finished) to 100 (finished)

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__

	def getName(self):
		return self.__name

	def updateScore(self):
		if self.isFinished():
			self.score = float("inf")
		else:
			self.score = float(self.__distance / (self.__priority * self.__points))
		return self.score

	def incrementFinished(self, by_value):
		self.__finished += int(by_value)

	def isFinished(self):
		if (self.__finished > self.FINISHED_THRESHOLD):
			True
		else:
			False

	def toXml(self):
		string =  "<goal name='" + self.__name + "'>\n\t<type>" + self.__type + "</type>\n"
		string += "\t<location-x>" + str(self.__location[0]) +"</location-x>\n\t<location-y>" + str(self.__location[1]) +"</location-y>\n"
		string += "\t<finished>" + str(self.__finished) + "</finished>\n\t<executions>\n\t"
		for execution in self.executions:
			string += execution.toXml()
		string += "\t</executions>\n</goal>\n"
		return string
