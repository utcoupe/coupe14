class Goal():
	def __init__(self, name='Abstract', points=0, priority=0):
		self.__priority = priority # Bigger is higger
		self.__distance = Infinity
		self.__points = points
		self.__name = name
		self.finished = 0
		self.score = 0

	def updateDistance(self):
		pass #TODO

	def updateScore(self):
		return self.score = 0 if finished
		return self.score = (__priority * __points)/ __distance

	def incrementFinished(self, by_value):
		self.finished += by_value

	def __cmp__(self, other):
		return self.score - other.score