# -*- coding: utf-8 -*-
"""
Class used to manage goals and find best execution
It is also a goal factory as it creates and save goals
This should be the only interface in the goals module
"""

import heapq
import logging
from xml.dom.minidom import parseString
from collections import deque

from .goal import *
from .goalExecution import *
from .ElemGoal import *
import os



class GoalsManager:
	def __init__(self, SubProcessManager, connection, robot_name):
		self.__robot_name 		= robot_name
		self.__logger			= logging.getLogger(__name__)

		self.__available_goals	= [] #List of available goals
		self.__blocked_goals	= [] # List of blocked goals
		self.__finished_goals	= [] #List of finished goals
		self.__elem_script		= {}

		self.__SubProcessManager = SubProcessManager
		self.__loadElemScript("elemScripts.xml")
		self.__loadGoals("goals.xml")
		self.__collectEnemyFinished()

		self.__loadScript()

	def goalFinishedId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__finishGoal(objectif)

	def goalCanceledId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__releaseGoal(objectif)

	def __blockGoalFromId(self, id_objectif):
		"""utilisé uniquement au chargement du script initial"""
		for goal in self.__available_goals:
			if goal.getId() == id_objectif:
				self.__blockGoal(goal)

	def __blockGoal(self, goal):
		self.__blocked_goals.append(goal)
		self.__available_goals.remove(goal)
		self.__logger.info('Goal ' + goal.getName() + ' is blocked')

	def __releaseGoal(self, goal):
		self.__available_goals.append(goal)
		self.__blocked_goals.remove(goal)
		self.__logger.info('Goal ' + goal.getName() + ' is released')

	def __finishGoal(self, goal):
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
			id				= int(xml_goal.getElementsByTagName('id')[0].firstChild.nodeValue) #nom explicite
			name 			= str(xml_goal.getElementsByTagName('name')[0].firstChild.nodeValue) #nom explicite
			type			= str(xml_goal.getElementsByTagName('type')[0].firstChild.nodeValue) #triangle, 
			concerned_robot = str(xml_goal.getElementsByTagName('concerned_robot')[0].firstChild.nodeValue) #ALL, TIBOT, FLUSSMITTEL
			x				= int(xml_goal.getElementsByTagName('x')[0].firstChild.nodeValue)
			y				= int(xml_goal.getElementsByTagName('y')[0].firstChild.nodeValue)

			#On ajoute uniquement les objectifs qui nous concerne
			if concerned_robot == "ALL" or concerned_robot == self.__robot_name:
				goal = Goal(id, name, type, concerned_robot, x, y)
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
	
	def __loadScript(self):
		if self.__robot_name == 'FLUSSMITTEL':
			script_filename = "data/script_flussmittel.xml"
		elif self.__robot_name == 'TIBOT':
			script_filename = "data/script_tibot.xml"

		self.__logger.info("loading actionScript from: " + str(script_filename))
		fd = open(script_filename,'r')
		dom = parseString(fd.read())
		fd.close()

		id_objectif_prev = 0
		for xml_goal in dom.getElementsByTagName('objectif'):
			objectif_name	= xml_goal.attributes["objectif_name"].value #seulement pour information
			id_objectif		= int(xml_goal.getElementsByTagName('idd')[0].firstChild.nodeValue)

			data_objectif = deque()
			for xml_execution in xml_goal.getElementsByTagName('action'):
				ordre 		= (xml_execution.getElementsByTagName('ordre')[0].firstChild.nodeValue,)

				raw_arguments = xml_execution.getElementsByTagName('arguments')[0].firstChild
				if raw_arguments:
					arguments = (raw_arguments.nodeValue.split(','),)
				else:
					arguments = (None,)

				ordre += arguments
				data_objectif.append(ordre)

			self.__blockGoalFromId(id_objectif)
			self.__SubProcessManager.sendGoal(id_objectif_prev, id_objectif, data_objectif)
			id_objectif_prev = id_objectif



