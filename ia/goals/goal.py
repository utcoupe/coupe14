class Goal():
	FINISHED_THRESHOLD = 50

	def __init__(self, name='Abstract', location=[0,0], orientation=0, points=0, priority=0, actions=[]):
		self.__name			= name
		self.__location 	= location
		self.__orientation	= orientation # 0-360° (0 is x axis, 90 is y axis)
		self.__points		= points
		self.__priority		= priority # Bigger is higher
		self.__actions		= actions
		self.__distance		= Infinity
		self.__finished		= 0 # From 0 (not finished) to 100 (finished)
		self.score			= 0
		self.routing		= -1

	def __updateRouting(self, current_pos):
		pass #TODO call navigation

	def updateDistance(self, current_pos):
		__updateRouting(current_pos)
		#TODO calculate distance from routing, this should be delegated to navigationn
		pass

	def updateScore(self):
		if bool(finished):
			self.score = Infinity
		else:
			self.score = __distance / (__priority * __points)
		return self.score

	def incrementFinished(self, by_value):
		self.__finished += int(by_value)

	def __cmp__(self, other):
		return self.score - other.score

	def getName(self):
		return self.name

	def isFinished(self):
		True if (finished > FINISHED_THRESHOLD) else False

	def toXml(self):
		__string =  "<goal name='" + __name + "'>\n"
		__string += "\t<points>" + __points + "</points>\n\t<location-x>" + __location[0] + "<location-x>\n"
		__string += "\t<location-x>" + __location[0] +"<location-y>\n\t<orientation>" + __orientation + "<orientation>\n"
		__string += "\t<priority>" + __priority + "</priority>\n\t<finished>" + 0 + "</finished>\n\t<actions>"
		for __action in __actions:
			__string += "\n\t\t<action>" + __action + "</action>"
		__string += "\n\t</actions>\n</goal>\n"
		return __string
