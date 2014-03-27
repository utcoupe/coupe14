# -*- coding: utf-8 -*-
"""
Class used to reprsent a goal
goal<-ElemGoal<-script
"""

from .constantes import *

class Goal:
	def __init__(self, name, typee, concerned_robot, x, y):
		self.__name 			= name
		self.__type				= typee
		self.__concerned_robot 	= concerned_robot
		self.__x 				= x
		self.__y 				= y
		self.__finished			= 0 # From 0 (not finished) to 100 (finished)

		self.__ElemGoal = []

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__

	def getName(self):
		return self.__name

	def incrementFinished(self, by_value):
		self.__finished += int(by_value)

	def isFinished(self):
		return (self.__finished > FINISHED_THRESHOLD)

	def appendElemGoal(self, ElemGoal):
		self.__ElemGoal.append(ElemGoal)




	"""def toXml(self):
		string =  "<goal name='" + self.__name + "'>\n\t<type>" + self.__type + "</type>\n"
		string += "\t<location-x>" + str(self.__location[0]) +"</location-x>\n\t<location-y>" + str(self.__location[1]) +"</location-y>\n"
		string += "\t<finished>" + str(self.__finished) + "</finished>\n\t<executions>\n\t"
		for execution in self.executions:
			string += execution.toXml()
		string += "\t</executions>\n</goal>\n"
		return string"""
