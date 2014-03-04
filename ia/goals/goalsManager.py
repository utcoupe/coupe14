# -*- coding: utf-8 -*-
import heapq
from xml.dom.minidom import parseString
from .goal import Goal

class GoalsManager:

	def __init__(self):
		self.__available_goals = []
		self.__finished_goals = []
		self.loadGoals()
		self.collectEnemyFinished()

		print "Available goals: %s" % self.__available_goals
		print "Finished goals: %s" % self.__finished_goals

	def __del__(self):
		self.saveGoals()

	def getBestGoal(self, current_pos):
		for goal in self.__available_goals:
			goal.updateDistance(current_pos)
			goal.updateScore()
		self.__available_goals.sort()
		print "GoalsManager:getBestGoal has chosen '%s'" % self.__available_goals[0].getName()
		return self.__available_goals[0]

	def setFinished(self, goal_name):
		for goal in self.__available_goals:
			if goal.getName == goal_name:
				goal.score = -float("inf")
				__available_goals.sort()
				__finished_goals.push(__available_goals.pop())
				print 'Goal ' + goal.getName() + ' has been maked finished'
				break
			else:
				raise 'Goal ' + goal.getName() + ' was not found when trying to be removed from heap'

	def collectEnemyFinished(self):
		for goal in self.__available_goals:
			print goal.isFinished()
			if goal.isFinished():
				print 'Goal ' + goal.getName() + ' has been calculated accomplished by the enemy'
				goal.score = -float("inf")
				self.__available_goals.sort()
				self.__finished_goals.push(self.__available_goals.pop())

	# XML import and export of goals
	def loadGoals(self, filename="goals/goals.xml"):
		print 'GoalsManager: loading goals from: %s' % filename
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()
		for xml_goal in dom.getElementsByTagName('goal'):
			name		= xml_goal.attributes["name"].value
			x 			= xml_goal.getElementsByTagName('location-x')[0].firstChild.nodeValue
			y			= xml_goal.getElementsByTagName('location-y')[0].firstChild.nodeValue
			orientation	= xml_goal.getElementsByTagName('orientation')[0].firstChild.nodeValue
			points		= xml_goal.getElementsByTagName('points')[0].firstChild.nodeValue
			priority	= xml_goal.getElementsByTagName('priority')[0].firstChild.nodeValue
			finished	= xml_goal.getElementsByTagName('finished')[0].firstChild.nodeValue
			actions		= []

			for xml_action in xml_goal.getElementsByTagName('action'):
				actions.append(xml_action.firstChild.nodeValue)

			goal = Goal(name, [x, y], orientation, points, priority, actions)
			goal.incrementFinished(finished)

			if goal.isFinished():
				self.__finished_goals.append(goal)
			else:
				self.__available_goals.append(goal)

		heapq.heapify(self.__available_goals)
		print "Available goals: %s" % self.__available_goals
		print "Finished goals: %s" % self.__finished_goals
	
	def saveGoals(self, filename='goals/saved_goals.xml'):
		print 'GoalsManager: saving goals to: ' + filename
		string = "<goals>\n"
		for heap in [self.__available_goals, self.__finished_goals]:
			for goal in heap:
				print goal.toXml()
				string += goal.toXml()
		string += "</goals>"

		doc = parseString(string) #Check XML validity
		with open(filename, "w") as f:
			f.write( doc.toxml() )
    		f.close()