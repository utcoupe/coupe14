# -*- coding: utf-8 -*-
"""
Class used to manage goals and find best execution
It is also a goal factory as it creates and save goals
This should be the only interface in the goals module
"""

import heapq
from xml.dom.minidom import parseString
from collections import OrderedDict
from .goal import Goal
from .goal import GoalExecution

class GoalsManager:

	def __init__(self):
		self.__available_goals	= [] #List of available goals
		self.__finished_goals	= [] #List of finished goals
		self.__blocked_goals	= [] # List of blocked goals
		self.__goal_types		= OrderedDict()
		self.loadGoals()
		self.collectEnemyFinished()

	def __del__(self):
		self.saveGoals()

	def getBestGoalExecution(self, current_pos):
		execution_heap = []
		for goal in self.__available_goals:
			for goal_execution in goal.executions:
				goal_execution.updateDistance(current_pos)
				goal_execution.updateScore()
				execution_heap.append(goal_execution)
				heapq.heapify(execution_heap)
		if not len(execution_heap):
			print('GoalsManager: no goal in available list')
			return -1 
		else:
			execution = heapq.heappop(execution_heap)
			associated_goal = execution.getGoal()
			self.__blockGoal(associated_goal)
			print("GoalsManager:getBestGoal has chosen '%s'" % associated_goal.getName())
			return execution

	def cancelExecution(self, execution):
		self.__releaseGoal(execution.getGoal())

	def finishExecution(self, execution):
		self.__finishGoal(execution.getGoal())

	def __blockGoal(self, goal):
		print(goal)
		self.__blocked_goals.append(goal)
		self.__available_goals.remove(goal)
		print('Goal ' + goal.getName() + ' was blocked')

	def __releaseGoal(self, goal):
		self.__available_goals.append(goal)
		self.__blocked_goals.remove(goal)
		print('Goal ' + goal.getName() + ' was released')

	def __finishGoal(self, goal):
		self.__finished_goals.append(goal)
		self.__blocked_goals.remove(goal)
		print('Goal ' + goal.getName() + ' was finished')

	def collectEnemyFinished(self):
		for goal in self.__available_goals:
			if goal.isFinished():
				print('Goal ' + goal.getName() + ' has been calculated accomplished by the enemy')
				self.__finishGoal(goal)

	# XML import and export of goals
	def loadGoals(self, filename="goals/goals.xml"):
		print('GoalsManager: loading goals from: %s' % filename)
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()
		for xml_goal in dom.getElementsByTagName('goal'):
			name		= xml_goal.attributes["name"].value
			type		= xml_goal.getElementsByTagName('type')[0].firstChild.nodeValue
			finished	= xml_goal.getElementsByTagName('finished')[0].firstChild.nodeValue
			gx 			= xml_goal.getElementsByTagName('location-x')[0].firstChild.nodeValue
			gy 			= xml_goal.getElementsByTagName('location-x')[0].firstChild.nodeValue

			goal = Goal(name, type, [gx, gy], [])
			goal.incrementFinished(finished)

			for xml_execution in xml_goal.getElementsByTagName('execution'):
				x 			= xml_execution.getElementsByTagName('location-x')[0].firstChild.nodeValue
				y			= xml_execution.getElementsByTagName('location-y')[0].firstChild.nodeValue
				orientation	= xml_execution.getElementsByTagName('orientation')[0].firstChild.nodeValue
				points		= xml_execution.getElementsByTagName('points')[0].firstChild.nodeValue
				priority	= xml_execution.getElementsByTagName('priority')[0].firstChild.nodeValue
				time		= xml_execution.getElementsByTagName('time')[0].firstChild.nodeValue
				actions		= []

				for action	in xml_execution.getElementsByTagName('action'):
					actions.append(action.firstChild.nodeValue)
				execution = GoalExecution(goal, [x, y], orientation, points, priority, actions, time)
				goal.executions.append(execution)

			if goal.isFinished():
				self.__finished_goals.append(goal)
			else:
				self.__available_goals.append(goal)
	
	def saveGoals(self, filename='../log/saved_goals.xml'):
		print('GoalsManager: saving goals to: ' + filename)
		string = "<goals>\n"
		for list in [self.__available_goals, self.__blocked_goals, self.__finished_goals]:
			for goal in list:
				string += goal.toXml()
		string += "</goals>"
		doc = parseString(string) #Check XML validity
		with open(filename, "w") as f:
			f.write( doc.toxml() )
			f.close()
