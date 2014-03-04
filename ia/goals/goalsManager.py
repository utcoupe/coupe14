
import heapq

class GoalsManager():
	FINISHED_LIMIT = 50

	def __init__(self):
		self.__available_goals = []
		self.__finished_goals = []

		#TODO load goals from xml & fill __available_goals
		heapq.heapify(__available_goals)

	def getBestGoal(self, current_pos):
		for goal in __available_goals
			goal.updateDistance(current_pos)
			goal.updateScore()
		__available_goals.sort()
		return __available_goals[0]
