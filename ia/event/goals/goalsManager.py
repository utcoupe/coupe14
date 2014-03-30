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
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "../..", "data"))

from .goal import *
from .goalExecution import *
from .ElemGoal import *
from .navigation import *



class GoalsManager:
	def __init__(self, SubProcessManager, connection, robot_name):
		self.__robot_name 		= robot_name
		self.__logger			= logging.getLogger(__name__)

		self.__available_goals		= [] #List of available goals
		self.__blocked_goals		= [] # List of blocked goals
		self.__finished_goals		= [] #List of finished goals
		self.__elem_script			= {}
		self.__SubProcessManager 	= SubProcessManager
		self.__last_id_objectif_send= 0

		data = self.__SubProcessManager.getData() #pas de self, data n'est pas stocké ici !
		#self.__PathFinding = PathFinding((data["FLUSSMITTEL"], data["TIBOT"], data["BIGENEMYBOT"], data["SMALLENEMYBOT"]))

		self.__loadElemScript("elemScripts.xml")
		self.__loadGoals("goals.xml")
		self.__collectEnemyFinished()

		self.__loadBeginScript()

	def goalFinishedId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__finishGoal(objectif)

	def goalCanceledId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__releaseGoal(objectif)

	def __addGoal(self, tuple_trajectoire_list, goal, elem_goal_id, prev_action=deque()):
		"""Méthode pour l'ajout d'un ordre dans la file du robot, la trajectoire envoyé ne doit pas contenir le point d'entrée"""
		if self.__tryBlockGoal(goal):
			#on met les prev_action, ce sont des hack pour faire passer le robot d'une action à l'autre avec un trajectoire prédeterminé
			orders = prev_action
			#on ajoute la trajectoire calculé
			orders.extend(self.__tupleTrajectoireToDeque(tuple_trajectoire_list))
			
			#on ajoute le point d'entré de l'objectif
			position = goal.getElemGoal(elem_goal_id).getPosition()
			got_to_position_finale = deque()
			got_to_position_finale.append(("A_GOTO", (position[0], position[1])))
			got_to_position_finale.append(("A_ROT", (position[2],)))
			orders.extend(got_to_position_finale)

			#on ajoute le script d'action
			orders.extend(self.__elem_script[ goal.getElemGoal(elem_goal_id).getIdScript() ])
			#on envoi le tout
			self.__SubProcessManager.sendGoal(self.__last_id_objectif_send, goal.getId(), orders)
			
			self.__last_id_objectif_send = goal.getId()
		else:
			self.__logger.error('Unable to block ' + goal.getName())

	def __tupleTrajectoireToDeque(self, tuple_trajectoire_list):
		order_list = deque()

		for tuple in tuple_trajectoire_list:
			order_list.append(('A_GOTO', [tuple[0], tuple[1]]))

		return order_list

	def __blockGoalFromId(self, id_objectif):
		"""utilisé uniquement au chargement du script initial"""
		for goal in self.__available_goals:
			if goal.getId() == id_objectif:
				self.__blockGoal(goal)

	def __tryBlockGoal(self, goal):
		if goal in self.__available_goals:
			self.__blocked_goals.append(goal)
			self.__available_goals.remove(goal)
			self.__logger.info('Goal ' + goal.getName() + ' is blocked')
			return True
		else:
			return False

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

	
	def __loadElemScript(self, filename):
		"""XML import of elementary scripts"""
		filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
		self.__logger.info(str(self.__robot_name) + ' is loading elementary scripts from: %s'% filename)
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()

		for elemScript in dom.getElementsByTagName('elemScript'):
			id_script 	= int(elemScript.getElementsByTagName('id_script')[0].firstChild.nodeValue) #nom explicite
			order_list 	= []
			for order in elemScript.getElementsByTagName('order'):
				raw_order = order.childNodes[0].nodeValue.split()
				order = raw_order[0]
				arguments = raw_order[1:]
				order_list.append((order, arguments))
			self.__elem_script[id_script] = order_list

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

				for elem_goal in xml_goal.getElementsByTagName('elem_goal'):
					id			= int(elem_goal.getElementsByTagName('id')[0].firstChild.nodeValue)
					x			= int(elem_goal.getElementsByTagName('x')[0].firstChild.nodeValue)
					y			= int(elem_goal.getElementsByTagName('y')[0].firstChild.nodeValue)
					angle		= float(elem_goal.getElementsByTagName('angle')[0].firstChild.nodeValue)
					points		= int(elem_goal.getElementsByTagName('points')[0].firstChild.nodeValue)
					priority	= int(elem_goal.getElementsByTagName('priority')[0].firstChild.nodeValue)
					duration	= int(elem_goal.getElementsByTagName('duration')[0].firstChild.nodeValue)
					id_script	= int(elem_goal.getElementsByTagName('id_script')[0].firstChild.nodeValue)
					#TODO instancier elem_goal
					goal.appendElemGoal( ElemGoal(id, x, y, angle, points, priority, duration, id_script) )

	def __loadBeginScript(self):
		if self.__robot_name == 'FLUSSMITTEL':
			script_filename = "data/script_flussmittel.xml"
		elif self.__robot_name == 'TIBOT':
			script_filename = "data/script_tibot.xml"

		self.__logger.info(str(self.__robot_name) + " loading beginScript from: " + str(script_filename))
		fd = open(script_filename,'r')
		dom = parseString(fd.read())
		fd.close()

		for xml_goal in dom.getElementsByTagName('objectif'):
			id_objectif	= int(xml_goal.getElementsByTagName('id_objectif')[0].firstChild.nodeValue)
			elem_goal_id= int(xml_goal.getElementsByTagName('elem_goal_id')[0].firstChild.nodeValue)

			prev_action = deque()
			for raw_prev_action in xml_goal.getElementsByTagName('prev_action'):
				raw_order = raw_prev_action.childNodes[0].nodeValue.split()
				order = raw_order[0]
				arguments = raw_order[1:]
				prev_action.append((order, arguments))

			find = False
			for goal in self.__available_goals:
				if goal.getId() == id_objectif:
					find = True
					self.__addGoal((), goal, elem_goal_id, prev_action=prev_action)
					break

			if not find:
				self.__logger.error(str(self.__robot_name) + " impossible de lui ajouter le goal d'id: " + str(id_objectif))
	
	"""def __loadScript(self):
		if self.__robot_name == 'FLUSSMITTEL':
			script_filename = "data/script_flussmittel.xml"
		elif self.__robot_name == 'TIBOT':
			script_filename = "data/script_tibot.xml"

		self.__logger.info(str(self.__robot_name) + " loading actionScript from: " + str(script_filename))
		fd = open(script_filename,'r')
		dom = parseString(fd.read())
		fd.close()

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
			self.__SubProcessManager.sendGoal(self.__last_id_objectif_send, id_objectif, data_objectif)
			self.__last_id_objectif_send = id_objectif
		"""



