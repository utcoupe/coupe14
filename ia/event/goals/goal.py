# -*- coding: utf-8 -*-
"""
Class used to reprsent a goal
A goal reprsent a task & contains a list of executions
It is loaded from XML file
"""


class Goal:
	FINISHED_THRESHOLD = 50

	def __init__(self, name, typee, concerned_robot, x, y, finished):
		print(name)
		self.__name 			= name
		self.__type				= typee
		self.__concerned_robot 	= concerned_robot
		self.__x 				= x
		self.__y 				= y
		self.__finished			= finished # From 0 (not finished) to 100 (finished)

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__

	def getName(self):
		return self.__name

	def incrementFinished(self, by_value):
		self.__finished += int(by_value)

	def isFinished(self):
		return (self.__finished > self.FINISHED_THRESHOLD)

	def appendElemGoal(self, x, y, angle, points, priority, duration, id_script):
		#TODO
		pass




	"""def toXml(self):
		string =  "<goal name='" + self.__name + "'>\n\t<type>" + self.__type + "</type>\n"
		string += "\t<location-x>" + str(self.__location[0]) +"</location-x>\n\t<location-y>" + str(self.__location[1]) +"</location-y>\n"
		string += "\t<finished>" + str(self.__finished) + "</finished>\n\t<executions>\n\t"
		for execution in self.executions:
			string += execution.toXml()
		string += "\t</executions>\n</goal>\n"
		return string"""
