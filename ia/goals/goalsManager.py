
import heapq

class GoalsManager():
	FINISHED_LIMIT = 50

	def __init__(self):
		self.__available_goals = []
		self.__finished_goals = []

		#TODO load goals from xml & fill __available_goals
		heapq.heapify(__available_goals)

	def getBestGoal(self, current_pos):
		for goal in __available_goals:
			goal.updateDistance(current_pos)
			goal.updateScore()
		__available_goals.sort()
		return __available_goals[0]

	def setFinished(self, goal_name):
		for goal in __available_goals:
			if goal.getName == goal_name:
				goal.score = -Infinity
				__available_goals.sort()
				__finished_goals.push(__available_goals.pop())
				print 'Goal ' + goal.getName() + ' has been maked finished'
				break
			else:
				raise 'Goal ' + goal.getName() + ' was not found when trying to be removed from heap'

	def collectEnemyFinished(self, goal):
		for goal in __available_goals:
			if goal.finished > FINISHED_LIMIT:
				print 'Goal ' + goal.getName() + ' has been calculated accomplished by the enemy'
				goal.score = -Infinity
				__available_goals.sort()
				__finished_goals.push(__available_goals.pop())

	def saveState(filename="saved_goals.xml"):
		pass #TODO