# -*- coding: utf-8 -*-
"""
Class used to reprsent an execution of a goal
It contains an entry-point, a time and a score calculated from context
GoalExecutions are compared on that score (lower is better choice)
"""

class GoalExecution:

	def __init__(self, goal, location, orientation, points, priority, actions, time):
		self.__location		= location
		self.__orientation	= float(orientation)
		self.__points		= int(points)
		self.__priority		= int(priority) # Bigger is higher
		self.__actions		= actions
		self.__distance		= float("inf")
		self.__time			= float(time)
		self.__goal			= goal
		self.score			= 0.0
		self.routing		= -1

	def getGoal(self):
		return self.__goal

	def __updateRouting(self, current_pos):
		pass #TODO call navigation

	def updateDistance(self, current_pos):
		self.__updateRouting(current_pos)
		#TODO calculate distance from routing, this should be delegated to navigationn
		pass

	def updateScore(self):
		self.score = float(self.__distance / (self.__priority * self.__points))

	def __cmp__(self, other):
		return self.score - other.score

	def toXml(self):
		string =  "<execution>\n"
		string += "\t<points>" + str(self.__points) + "</points>\n\t<location-x>" + str(self.__location[0]) + "</location-x>\n"
		string += "\t<location-y>" + str(self.__location[1]) +"</location-y>\n\t<orientation>" + str(self.__orientation) + "</orientation>\n"
		string += "\t<score>" + str(self.score) + "</score>\n"
		string += "\t<priority>" + str(self.__priority) + "</priority>\n\t<time>" + str(self.__time) + "</time>\n\t<actions>"
		for action in self.__actions:
			string += "\n\t\t<action>" + str(action) + "</action>"
		string += "\n\t</actions>\n\t</execution>\n"
		return string