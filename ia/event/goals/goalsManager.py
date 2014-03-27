# -*- coding: utf-8 -*-
"""
Class used to manage goals and find best execution
It is also a goal factory as it creates and save goals
This should be the only interface in the goals module
"""

import heapq
import logging
from xml.dom.minidom import parseString

from .goal import *
from .goalExecution import *
from .ElemGoal import *
import os



class GoalsManager:
	def __init__(self, robot_name):
		self.__robot_name 		= robot_name
		self.__logger			= logging.getLogger(__name__)

		self.__available_goals	= [] #List of available goals
		self.__blocked_goals	= [] # List of blocked goals
		self.__finished_goals	= [] #List of finished goals
		self.__elem_script		= {}

		self.__loadElemScript("elemScripts.xml")
		self.__loadGoals("goals.xml")
		self.__collectEnemyFinished()

	def blockGoal(self, goal):
		self.__blocked_goals.append(goal)
		self.__available_goals.remove(goal)
		self.__logger.info('Goal ' + goal.getName() + ' is blocked')

	def releaseGoal(self, goal):
		self.__available_goals.append(goal)
		self.__blocked_goals.remove(goal)
		self.__logger.info('Goal ' + goal.getName() + ' is released')

	def finishGoal(self, goal):
		self.__finished_goals.append(goal)
		self.__blocked_goals.remove(goal)
		self.__logger.info('Goal ' + goal.getName() + ' is finished')

	def __collectEnemyFinished(self):
		for goal in self.__available_goals:
			if goal.isFinished():
				self.__logger.info('Goal ' + goal.getName() + ' has been calculated as accomplished by the enemy')
				self.finishGoal(goal)

	def __loadGoals(self, filename):
		"""XML import of goals"""
		filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
		self.__logger.info(str(self.__robot_name) + ' is loading goals from: %s'% filename)
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()

		for xml_goal in dom.getElementsByTagName('goal'):
			name 			= str(xml_goal.getElementsByTagName('name')[0].firstChild.nodeValue) #nom explicite
			typee			= str(xml_goal.getElementsByTagName('typee')[0].firstChild.nodeValue) #triangle, 
			concerned_robot = str(xml_goal.getElementsByTagName('concerned_robot')[0].firstChild.nodeValue) #ALL, TIBOT, FLUSSMITTEL
			x				= int(xml_goal.getElementsByTagName('x')[0].firstChild.nodeValue)
			y				= int(xml_goal.getElementsByTagName('y')[0].firstChild.nodeValue)

			#On ajoute uniquement les objectifs qui nous concerne
			if concerned_robot == "ALL" or concerned_robot == self.__robot_name:
				goal = Goal(name, typee, concerned_robot, x, y)
				self.__available_goals.append(goal)

				for elem_goal in dom.getElementsByTagName('elem_goal'):
					x			= int(elem_goal.getElementsByTagName('x')[0].firstChild.nodeValue)
					y			= int(elem_goal.getElementsByTagName('y')[0].firstChild.nodeValue)
					angle		= float(elem_goal.getElementsByTagName('angle')[0].firstChild.nodeValue)
					points		= int(elem_goal.getElementsByTagName('points')[0].firstChild.nodeValue)
					priority	= int(elem_goal.getElementsByTagName('priority')[0].firstChild.nodeValue)
					duration	= int(elem_goal.getElementsByTagName('duration')[0].firstChild.nodeValue)
					id_script	= int(elem_goal.getElementsByTagName('id_script')[0].firstChild.nodeValue)
					#TODO instancier elem_goal
					goal.appendElemGoal( ElemGoal(x, y, angle, points, priority, duration, id_script) )
	
	def __loadElemScript(self, filename):
		"""XML import of elementary scripts"""
		filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
		self.__logger.info(str(self.__robot_name) + ' is loading elementary scripts from: %s'% filename)
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()

		for elemScript in dom.getElementsByTagName('elemScript'):
			id_script 		= str(elemScript.getElementsByTagName('id_script')[0].firstChild.nodeValue) #nom explicite
			order_list = []
			for order in dom.getElementsByTagName('order'):
				order_list.append(order.childNodes[0].nodeValue)
			self.__elem_script[id_script] = order_list
			


	"""def getBestGoalExecution(self, current_pos):
		execution_heap = []
		for goal in self.__available_goals:
			for goal_execution in goal.executions:
				goal_execution.updateDistance(current_pos)
				goal_execution.updateScore()
				execution_heap.append(goal_execution)
				heapq.heapify(execution_heap)
		if not len(execution_heap):
			self.__logger.warning("no goal in available list")
			return -1 
		else:
			execution = heapq.heappop(execution_heap)
			associated_goal = execution.getGoal()
			self.__blockGoal(associated_goal)
			self.__logger.info("getBestGoal has chosen '%s'" % associated_goal.getName())
			return execution"""
	
	"""def saveGoals(self, filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../log/saved_goals.xml")):
		self.__logger.info('GoalsManager: saving goals to: ' + filename)
		string = "<goals>\n"
		for list in [self.__available_goals, self.__blocked_goals, self.__finished_goals]:
			for goal in list:
				string += goal.toXml()
		string += "</goals>"
		doc = parseString(string) #Check XML validity
		with open(filename, "w") as f:
			f.write( doc.toxml() )
			f.close()"""
