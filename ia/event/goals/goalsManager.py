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
import inspect, os


from .goal import *
from .goalExecution import *
from .ElemGoal import *
from .navigation import *



class GoalsManager:
	def __init__(self, SubProcessManager, connection, robot_name):
		base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		self.__robot_name 		= robot_name
		self.__logger			= logging.getLogger(__name__)

		self.__available_goals		= [] #List of available goals
		self.__blocked_goals		= [] # List of blocked goals
		self.__goto_finished_goals	= [] # List of blocked goals
		self.__finished_goals		= [] #List of finished goals
		self.__elem_script			= {}
		self.__SubProcessManager 	= SubProcessManager
		self.__last_id_objectif_send= 0

		self.__back_triangle_stack = deque()
		self.__front_triangle_stack = deque()

		data = self.__SubProcessManager.getData() #pas de self, data n'est pas stocké ici !
		self.__our_color = data["METADATA"]["getOurColor"]
		self.__PathFinding = PathFinding((data["FLUSSMITTEL"], data["TIBOT"], data["BIGENEMYBOT"], data["SMALLENEMYBOT"]))

		self.__loadElemScript(base_dir+"/elemScripts.xml")
		self.__loadGoals(base_dir+"/goals.xml")
		self.__collectEnemyFinished()

		self.__reverse_table = {}
		self.__reverse_table[(0,0)] = (1,1)
		self.__reverse_table[(1,1)] = (0,0)
		self.__reverse_table[(0,1)] = (1,0)
		self.__reverse_table[(1,0)] = (0,1)

		self.__reverse_table[(9,0)] = (2,0)
		self.__reverse_table[(2,0)] = (9,0)

		self.__reverse_table[(8,0)] = (3,0)
		self.__reverse_table[(3,0)] = (8,0)
		self.__reverse_table[(8,1)] = (3,1)
		self.__reverse_table[(3,1)] = (8,1)

		self.__reverse_table[(7,0)] = (4,1)
		self.__reverse_table[(4,1)] = (7,0)
		self.__reverse_table[(7,1)] = (4,0)
		self.__reverse_table[(4,0)] = (7,1)

		self.__reverse_table[(6,0)]=(5,0)
		self.__reverse_table[(5,0)]=(6,0)

		self.__loadBeginScript()

	def __queueBestGoals(self):
		if not self.__blocked_goals:
			data = self.__SubProcessManager.getData()
			self.__PathFinding.update(data[self.__robot_name])
			if self.__available_goals:
				goal = self.__available_goals[0]
				path = self.__getOrderTrajectoire(data, goal, 0)
				self.__addGoal(path, goal, 0)

	def processStorageStatus(self, status):
		executed_without_faillure = status[0]
		color = status[1]
		position = status[2]
		
		if executed_without_faillure:
			if position == "FRONT":
				self.__front_triangle_stack.append(color)
			else:
				self.__back_triangle_stack.append(color)
		else:
			#TODO
			pass

	def goalFinishedId(self, id_objectif):
		for objectif in self.__goto_finished_goals:
			if objectif.getId() == id_objectif:
				self.__finishGoal(objectif) 
			self.__queueBestGoals()

	def goalGotoFinishedId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__gotoFinishGoal(objectif)

	def goalCanceledId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__releaseGoal(objectif)
			self.__queueBestGoals()

	def __addGoal(self, tuple_trajectoire_list, goal, elem_goal_id, prev_action=None):
		"""Méthode pour l'ajout d'un ordre dans la file du robot"""
		if self.__tryBlockGoal(goal, elem_goal_id):
			#on met les prev_action, ce sont des hack pour faire passer le robot d'une action à l'autre avec un trajectoire prédeterminé
			if prev_action is None:
				orders = deque()
			else:
				orders = prev_action

			#on ajoute la trajectoire calculé
			orders.extend(self.__tupleTrajectoireToDeque(tuple_trajectoire_list))
			orders.append( ("A_ROT", (goal.getElemGoal(elem_goal_id).getPositionAndAngle()[2],),) )
			#on ajoute attend d'être arrivé pour lancer les actions
			orders.append( ("END_GOTO", (),) )
			orders.append( ("GOTO_OVER", (),) )
			#on ajoute le script d'action
			orders.extend(self.__elem_script[ goal.getElemGoalLocked().getIdScript() ])
			#on ajoute un marqueur de fin
			orders.append( ("END", (),) )
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

	def __tryBlockGoal(self, goal, elem_goal_id):
		if goal in self.__available_goals:
			self.__available_goals.remove(goal)
			self.__blocked_goals.append(goal)
			goal.setElemGoalLocked(goal.getElemGoal(elem_goal_id))
			self.__logger.info('Goal ' + goal.getName() + ' is blocked')
			return True
		else:
			return False

	def __releaseGoal(self, goal):
		self.__blocked_goals.remove(goal)#On ne peut pas enlever les ordres dans self.__goto_finished_goals
		self.__available_goals.append(goal)
		self.__logger.info('Goal ' + goal.getName() + ' is released')

	def __gotoFinishGoal(self, goal):
		self.__blocked_goals.remove(goal)
		self.__goto_finished_goals.append(goal)
		self.__logger.info('Goal ' + goal.getName() + ' is goto finished')

	def __finishGoal(self, goal):
		"""if end_status:
			action_type = end_status[0]
			color = end_status[1]
			load_point = end_status[2]

			if load_point == "BACK":
				if action_type == "LOAD":
					self.__back_triangle_stack.append(color)
				elif action_type == "UNLOAD":
					self.__back_triangle_stack.popleft()
				else:
					self.__logger.error("Action inconnu, action_type: "+str(action_type))

			elif load_point == "FRONT":
				if action_type == "LOAD":
					self.__front_triangle_stack.append(color)
				elif action_type == "UNLOAD":
					self.__front_triangle_stack.popleft()
				else:
					self.__logger.error("Action inconnu, action_type: "+str(action_type))

			else:
				self.__logger.error("On a chargé une couleur inconnu color: "+str(color))"""
				
		self.__goto_finished_goals.remove(goal)
		self.__finished_goals.append(goal)
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
					color		= str(elem_goal.getElementsByTagName('color')[0].firstChild.nodeValue)
					id_script	= int(elem_goal.getElementsByTagName('id_script')[0].firstChild.nodeValue)
					#TODO instancier elem_goal
					goal.appendElemGoal( ElemGoal(id, x, y, angle, points, priority, duration, color, id_script) )

	def __loadBeginScript(self):
		base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		if self.__robot_name == 'FLUSSMITTEL':
			script_filename = base_dir+"/../../data/script_flussmittel.xml"
		elif self.__robot_name == 'TIBOT':
			script_filename = base_dir+"/../../data/script_tibot.xml"

		self.__logger.info(str(self.__robot_name) + " loading beginScript from: " + str(script_filename))
		fd = open(script_filename,'r')
		dom = parseString(fd.read())
		fd.close()

		data = self.__SubProcessManager.getData()
		self.__PathFinding.update(data[self.__robot_name])

		for xml_goal in dom.getElementsByTagName('objectif'):
			id_objectif	= int(xml_goal.getElementsByTagName('id_objectif')[0].firstChild.nodeValue)
			elem_goal_id= int(xml_goal.getElementsByTagName('elem_goal_id')[0].firstChild.nodeValue)

			position_depart_sepciale = None
			#Inversion du script
			if self.__our_color == "YELLOW":
				id_objectif, elem_goal_id = self.__reverse_table[(id_objectif, elem_goal_id)]
			prev_action = deque()
			for raw_prev_action in xml_goal.getElementsByTagName('prev_action'):
				raw_order = raw_prev_action.childNodes[0].nodeValue.split()
				order = str(raw_order[0])
				arguments = raw_order[1:]
				if order == "MYPOSITION_INFO":
					if self.__our_color == "RED":
						position_depart_sepciale = (int(arguments[0]), int(arguments[1]), float(arguments[2]))
					else:
						position_depart_sepciale = (3000 - int(arguments[0]), int(arguments[1]), float(arguments[2]))
				else:
					prev_action.append((order, arguments))

			find = False
			for goal in self.__available_goals:
				if goal.getId() == id_objectif:
					find = True
					path = self.__getOrderTrajectoire(data, goal, elem_goal_id, position_depart_sepciale)
					if path != []:
						self.__addGoal(path, goal, elem_goal_id, prev_action=prev_action)
					else:
						self.__logger.info(str(self.__robot_name) + " Aucun chemin disponible vers " +str(goal.getElemGoal(elem_goal_id).getPositionAndAngle())+" pour le goal d'id: " + str(id_objectif))
					break

			if not find:
				self.__logger.error(str(self.__robot_name) + " impossible de lui ajouter le goal d'id: " + str(id_objectif))
	
	def __getOrderTrajectoire(self, data, goal, elem_goal_id, position_depart_sepciale=None):
		"""Il faut mettre à jour les polygones avant d'utiliser cette fonction"""
		if position_depart_sepciale is not None:
			position_last_goal = position_depart_sepciale
			self.__logger.debug("Position from position_depart_sepciale" + str(position_last_goal))
		elif self.__blocked_goals:
			last_goal = self.__blocked_goals[-1]
			position_last_goal = last_goal.getElemGoalLocked().getPositionAndAngle()
			self.__logger.debug("Position from queue" + str(position_last_goal))
		else:
			position_last_goal = data[self.__robot_name]["getPositionAndAngle"]
			self.__logger.debug("Position from data" + str(position_last_goal))

		position_to_reach = goal.getElemGoal(elem_goal_id).getPositionAndAngle()
		path = self.__PathFinding.getPath((position_last_goal[0], position_last_goal[1]), (position_to_reach[0], position_to_reach[1]), enable_smooth=True)

		return path

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



