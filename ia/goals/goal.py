class Goal():
	def __init__(self, name='Abstract', location=[0,0], points=0, priority=0, actions=[]):
		self.__name		= name
		self.__location = location
		#TODO orientation ?
		self.__points	= points
		self.__priority	= priority # Bigger is higher
		self.__actions	= actions
		self.__distance	= Infinity
		self.finished	= 0 # From 0 (not finished) to 100 (finished)
		self.score		= 0
		self.routing	= -1

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
		self.finished += int(by_value)

	def __cmp__(self, other):
		return self.score - other.score

	def getName(self):
		return self.name