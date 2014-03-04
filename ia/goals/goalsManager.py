
import heapq
from xml.dom.minidom import parseString

class GoalsManager():

	def __init__(self):
		self.__available_goals = []
		self.__finished_goals = []
		loadGoals()

	def __del__(self):
		saveGoals()

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
			if goal.isFinished
				print 'Goal ' + goal.getName() + ' has been calculated accomplished by the enemy'
				goal.score = -Infinity
				__available_goals.sort()
				__finished_goals.push(__available_goals.pop())

	def loadGoals(filename='goals.xml'):
		print 'GoalsManager: loading goals from: ' + filename
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()
		for __xml_goal in dom.getElementsByTagName('goal'):
			__name			= __xml_goal.attributes["name"].value
			__x 			= __xml_goal.getElementsByTagName('location-x')[0].value
			__y				= __xml_goal.getElementsByTagName('location-y')[0].value
			__orientation	= __xml_goal.getElementsByTagName('orientation')[0].value
			__points		= __xml_goal.getElementsByTagName('points')[0].value
			__priority		= __xml_goal.getElementsByTagName('priority')[0].value
			__finished		= (bool __xml_goal.getElementsByTagName('finished')[0].value)
			__actions		= []

			for __xml_action in __xml_goal.getElementsByTagName('action'):
				__actions.append(__xml_action.value)

			__goal = Goal(__name, [__x, __y], __orientation, __points, __priority, __actions)
			__goal.incrementFinished(__finished)

			if __goal.isFinished():
				self.__available_goals.append(__goal)
			else:
				self.__finished_goals.append(__goal)

		heapq.heapify(__available_goals)
	
	def saveGoals(filename='saved_goals.xml'):
		print 'GoalsManager: saving goals to: ' + filename
		__string = "<goals>\n"
		for goal in self.__available_goals:
			__string += goal.toXml()
		__string += "</goals>"

		doc = parseString(__string) #Check XML validity
		with open(filename, "w") as f:
    		f.write( doc.toxml() )
    	f.close()