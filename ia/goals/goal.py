# -*- coding: utf-8 -*-

class Goal:
	FINISHED_THRESHOLD = 50

	def __init__(self, name='Abstract', location=[0,0], orientation=0, points=0, priority=0, actions=[]):
		self.__name			= name
		self.__location 	= location
		self.__orientation	= float(orientation) # 0-360° (0 is x axis, 90 is y axis)
		self.__points		= int(points)
		self.__priority		= int(priority) # Bigger is higher
		self.__actions		= actions
		self.__distance		= float("inf")
		self.__finished		= 0 # From 0 (not finished) to 100 (finished)
		self.score			= 0.0
		self.routing		= -1

	def __updateRouting(self, current_pos):
		pass #TODO call navigation

	def updateDistance(self, current_pos):
		self.__updateRouting(current_pos)
		#TODO calculate distance from routing, this should be delegated to navigationn
		pass

	def updateScore(self):
		if self.isFinished():
			self.score = float("inf")
		else:
			self.score = float(self.__distance / (self.__priority * self.__points))
		return self.score

	def incrementFinished(self, by_value):
		self.__finished += int(by_value)

	def __cmp__(self, other):
		return self.score - other.score

	def getName(self):
		return self.__name

	def isFinished(self):
		if (self.__finished > self.FINISHED_THRESHOLD):
			True
		else:
			False

	def toXml(self):
		string =  "<goal name='" + self.__name + "'>\n"
		string += "\t<points>" + str(self.__points) + "</points>\n\t<location-x>" + str(self.__location[0]) + "</location-x>\n"
		string += "\t<location-y>" + str(self.__location[0]) +"</location-y>\n\t<orientation>" + str(self.__orientation) + "</orientation>\n"
		string += "\t<priority>" + str(self.__priority) + "</priority>\n\t<finished>" + str(self.__finished) + "</finished>\n\t<actions>"
		for action in self.__actions:
			string += "\n\t\t<action>" + action + "</action>"
		string += "\n\t</actions>\n</goal>\n"
		return string
