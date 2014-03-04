# -*- coding: utf-8 -*-
import heapq
from xml.dom.minidom import parseString
import goal

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
			if goal.isFinished():
				print 'Goal ' + goal.getName() + ' has been calculated accomplished by the enemy'
				goal.score = -Infinity
				__available_goals.sort()
				__finished_goals.push(__available_goals.pop())

	# XML import and export of goals
	def loadGoals(filename='goals.xml'):
		print 'GoalsManager: loading goals from: ' + filename
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()
		for xml_goal in dom.getElementsByTagName('goal'):
			name		= xml_goal.attributes["name"].value
			x 			= xml_goal.getElementsByTagName('location-x')[0].value
			y			= xml_goal.getElementsByTagName('location-y')[0].value
			orientation	= xml_goal.getElementsByTagName('orientation')[0].value
			points		= xml_goal.getElementsByTagName('points')[0].value
			priority	= xml_goal.getElementsByTagName('priority')[0].value
			finished	= bool(xml_goal.getElementsByTagName('finished')[0].value)
			actions		= []

			for xml_action in xml_goal.getElementsByTagName('action'):
				actions.append(xml_action.value)

			goal = Goal(name, [x, y], orientation, points, priority, actions)
			goal.incrementFinished(finished)

			if goal.isFinished():
				self.__available_goals.append(goal)
			else:
				self.__finished_goals.append(goal)

		heapq.heapify(__available_goals)
	
	def saveGoals(filename='saved_goals.xml'):
		print 'GoalsManager: saving goals to: ' + filename
		string = "<goals>\n"
		for goal in self.__available_goals:
			string += goal.toXml()
		string += "</goals>"

		doc = parseString(string) #Check XML validity
		with open(filename, "w") as f:
			f.write( doc.toxml() )
    		f.close()