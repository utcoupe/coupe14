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
from .ElemGoal import *
from .navigation import *
from .visio import *


class GoalsManager:
	def __init__(self, SubProcessManager, connection, robot_name):
		base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		self.__robot_name 		= robot_name
		self.__logger			= logging.getLogger(__name__)

		self.__available_goals		= [] #List of available goals
		self.__blocked_goals		= [] # List of blocked goals
		self.__dynamique_finished_goals	= [] # List of blocked goals
		self.__finished_goals		= [] #List of finished goals
		self.__elem_script			= {}
		self.__SubProcessManager 	= SubProcessManager
		self.__last_id_objectif_send= None

		self.__back_triangle_stack = deque()
		self.__front_triangle_stack = deque()

		self.__data = self.__SubProcessManager.getData()
		self.__our_color = self.__data["METADATA"]["getOurColor"]
		self.__PathFinding = PathFinding((self.__data["FLUSSMITTEL"], self.__data["TIBOT"], self.__data["BIGENEMYBOT"], self.__data["SMALLENEMYBOT"]))

		self.__loadElemScript(base_dir+"/elemScripts.xml")
		self.__loadGoals(base_dir+"/goals.xml")

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

		self.__reverse_table[(10,0)]=(10,1)

		if self.__robot_name == "FLUSSMITTEL":
			self.__vision = Visio('../supervisio/build/visio', 0, '../supervisio/', self.__data["FLUSSMITTEL"])
			self.__last_camera_color = None

		self.__loadBeginScript()

	def __queueBestGoals(self):
		if not self.__blocked_goals:
			self.__logger.debug(str(self.__robot_name)+" Recherche d'un nouvel objectif")	
			self.__PathFinding.update(self.__data[self.__robot_name])
			if self.__available_goals:
				goal = self.__available_goals[0]
				path = self.__getOrderTrajectoire(goal, 0)
				self.__addGoal(path, goal, 0)
			else:
				self.__logger.warning(str(self.__robot_name)+" N'a plus aucun objectif disponible, GG !")

	#GOAL management from ID
	def __blockGoalFromId(self, id_objectif):
		"""utilisé uniquement au chargement du script initial"""
		for goal in self.__available_goals:
			if goal.getId() == id_objectif:
				self.__blockGoal(goal)
				break

	def goalStepOverId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__manageStepOver(objectif, id_objectif, skip_get_triangle=False)
				break

	def goalDynamiqueFinishedId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__blocked_goals.remove(objectif)
				self.__dynamique_finished_goals.append(objectif)
				break

	def goalCanceledId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__cancelGoal(objectif)
				break

	def goalFinishedId(self, id_objectif):
		for objectif in self.__dynamique_finished_goals:
			if objectif.getId() == id_objectif:
				self.__finishGoal(objectif) 

	#GOAL management from GOAL
	def __tryBlockGoal(self, goal, elem_goal_id):
		if goal in self.__available_goals:
			self.__available_goals.remove(goal)
			self.__blocked_goals.append(goal)
			goal.setElemGoalLocked(goal.getElemGoal(elem_goal_id))
			self.__logger.info('Goal '+goal.getName()+' id: '+str(goal.getId())+' is blocked')
			return True
		else:
			self.__logger.warning('Goal '+goal.getName()+' id: '+str(goal.getId())+" n'a pas pu être bloqué")
			return False

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
			orders.append( ("A_ROT", (goal.getElemGoal(elem_goal_id).getPositionAndAngle()[2],)) )
			#on ajoute attend d'être arrivé pour lancer les actions
			orders.append( ("THEN", ()) )
			orders.append( ("STEP_OVER", ()) )

			#on envoi le tout
			self.__SubProcessManager.sendGoal(self.__last_id_objectif_send, goal.getId(), orders)
			self.__last_id_objectif_send = goal.getId()
		else:
			#TODO, ce cas peut-il vrament arrivé ?
			self.__logger.warning("On va rechercher un nouvel ordre")
			self.__queueBestGoals()

	def __cancelGoal(self, goal):
		self.__blocked_goals.remove(goal)#On ne peut pas enlever les ordres dans self.__dynamique_finished_goals
		self.__available_goals.append(goal)
		self.__logger.info('Goal ' + goal.getName() + ' has been canceled and is now released')
		self.__SubProcessManager.sendDeleteGoal(goal.getId())
		self.__queueBestGoals()


	def __finishGoal(self, goal):		
		self.__dynamique_finished_goals.remove(goal)
		self.__finished_goals.append(goal)
		self.__logger.info('Goal ' + goal.getName() + ' is finished')
		self.__queueBestGoals()

	def __deleteGoal(self, goal):
		success = False

		if goal in self.__available_goals:
			self.__available_goals.remove(goal)
			success = True
		if goal in self.__blocked_goals:
			self.__blocked_goals.remove(goal)
			success = True
		if goal in self.__dynamique_finished_goals:
			self.__dynamique_finished_goals.remove(goal)
			success = True
		if goal in self.__finished_goals:
			self.__finished_goals.remove(goal)
			success = True

		self.__SubProcessManager.sendDeleteGoal(goal.getId())
		if success:
			self.__logger.info('Goal ' + goal.getName() + ' is delete')
		else:
			self.__logger.error('Goal ' + goal.getName() + " can't be delete")
		self.__queueBestGoals()

	def __manageStepOver(self, objectif, id_objectif, skip_get_triangle=False):
		action_list = objectif.getElemGoalLocked().getFirstElemAction()
		if action_list:
			if action_list[0][0] == "GET_TRIANGLE_IA" and self.__robot_name == "FLUSSMITTEL":#Redondant normalement
				if skip_get_triangle == True:
					position = None # 1=front and -1=back
					hauteur = None #hauteur en mm
					nb_front_stack = len(self.__front_triangle_stack) 
					nb_back_stack = len(self.__back_triangle_stack)
					stack_full = False
					script_to_send = deque()

					if self.__our_color == self.__last_camera_color:
						if nb_front_stack < MAX_FRONT_TRIANGLE_STACK:
							self.__front_triangle_stack.append(self.__last_camera_color)
							position = 1
							hauteur = GARDE_AU_SOL + nb_front_stack*HAUTEUR_TRIANGLE + MARGE_DROP_TRIANGLE
						else:
							self.__logger.error("On a pas la place pour stocker ce triangle à l'avant, ca cas ne devrait pas arriver !")
							stack_full = True
							self.__cancelGoal(objectif)

					else:
						if (nb_front_stack < MAX_FRONT_TRIANGLE_STACK) and (nb_back_stack < MAX_BACK_TRIANGLE_STACK):
							self.__back_triangle_stack.append(self.__last_camera_color)
							position = -1
							hauteur = GARDE_AU_SOL + nb_front_stack*HAUTEUR_TRIANGLE + MARGE_DROP_TRIANGLE #ici c'est bien nb_front_stack !
						elif (nb_front_stack < MAX_FRONT_TRIANGLE_STACK) and (nb_back_stack >= MAX_BACK_TRIANGLE_STACK):
							self.__back_triangle_stack.popleft()
							script_to_send.append( ("O_RET_OUVRIR", ()) )
							self.__back_triangle_stack.append(self.__last_camera_color)
							position = -1
							hauteur = GARDE_AU_SOL + nb_front_stack*HAUTEUR_TRIANGLE + MARGE_DROP_TRIANGLE #ici c'est bien nb_front_stack !
						else:
							self.__logger.error("On a pas la place pour stocker ce triangle ni à l'avant ni à l'arrière, ce cas ne devrait pas arriver !")
							stack_full = True
							self.__cancelGoal(objectif)

					if not stack_full:
						script_base = action_list
						for action in script_base:
							if action[0] == "STORE_TRIANGLE_IA":
								script_to_send.append( ("O_STORE_TRIANGLE", (int(position*hauteur),)) )
							elif action[0] == "GET_TRIANGLE_IA":
								pass
							else:
								script_to_send.append(action)
						self.__SubProcessManager.sendGoal(objectif.getId(), objectif.getId(), script_to_send)
						objectif.getElemGoalLocked().removeFirstElemAction()

				else:
					#self.__vision.update()
					#triangle_list = self.__vision.getTriangles()


					#TODO remove this bypass:
					#if triangle_list == []:
					if False:

						self.__logger.warning("On a pas vu de triangle à la position attendu, dont on va supprimer l'objectif "+str(id_objectif))
						self.__last_camera_color = None
						self.__deleteGoal(objectif)
					else:
						#TODO remove this bypass:
						#triangle = triangle_list[0] #TODO, prendre le meilleur triangle suivent les arg
						#data_camera = (triangle.color, triangle.coord[0], triangle.coord[1]) #type (color, x, y)
						data_camera = ("RED", 10, 10)


						self.__last_camera_color = data_camera[0]

						#si on aura la possibilité de le stcker
						if len(self.__front_triangle_stack)  >= MAX_FRONT_TRIANGLE_STACK:
							self.__logger.warning("Impossible de stocker ce triangle dans le robot, la pile de devant est pleine.")
							#Si besoin, on change la couleur du triangle pour la prochaine fois
							if self.__last_camera_color != objectif.getColorElemLock():
								objectif.switchColor()
							self.__cancelGoal(objectif)
						else:
							if self.__positionReady(data_camera[1], data_camera[2]):
								script_get_triangle = deque()
								script_get_triangle.append( ("O_GET_TRIANGLE", (data_camera[1], data_camera[2], HAUTEUR_TORCHE+3*HAUTEUR_TRIANGLE)) ) #TODO hauteur par triangle dans le cas des triangles au sol
								script_get_triangle.append( ("THEN", ()) )
								script_get_triangle.append( ("O_GET_BRAS_STATUS", ()) )
								script_get_triangle.append( ("THEN", (),) )
								self.__SubProcessManager.sendGoal(objectif.getId(), objectif.getId(), script_get_triangle)
			else:
				self.__SubProcessManager.sendGoal(objectif.getId(), objectif.getId(), action_list)
				objectif.getElemGoalLocked().removeFirstElemAction()
		else:
			self.__logger.warning("Pb, Il y a un STEP_OVER directement suivit d'un END ?")

	def __positionReady(self, x, y):
		#TODO
		return True

	def processBrasStatus(self, status_fin, id_objectif):
		objectif = None
		for objectif_temp in self.__blocked_goals:
			if objectif_temp.getId() == id_objectif:
				objectif = objectif_temp

		if objectif is None:
			self.__logger.critical("L'objectif a supprimer n'est plus dans la liste des bloqués "+str(id_objectif))
		else:
			if status_fin == 1:
				self.__manageStepOver(objectif, id_objectif, skip_get_triangle=True)
			else:
				self.__logger.warning("La prehention du trianglé à échoué, donc on supprime l'ordre"+str(id_objectif))
				self.__deleteGoal(objectif)


	#TODO utiliser cette focntion ?
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
			order_list 	= deque()
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
					goal.appendElemGoal( ElemGoal(id, x, y, angle, points, priority, duration, color, self.__elem_script[id_script]) )

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

		self.__PathFinding.update(self.__data[self.__robot_name])

		for xml_goal in dom.getElementsByTagName('objectif'):
			id_objectif	= int(xml_goal.getElementsByTagName('id_objectif')[0].firstChild.nodeValue)
			elem_goal_id= int(xml_goal.getElementsByTagName('elem_goal_id')[0].firstChild.nodeValue)

			position_depart_speciale = None
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
						position_depart_speciale = (int(arguments[0]), int(arguments[1]), float(arguments[2]))
					else:
						position_depart_speciale = (3000 - int(arguments[0]), int(arguments[1]), float(arguments[2]))
				elif order == "A_GOTO" and self.__our_color == "YELLOW":
					arg = (3000 - int(arguments[0]), int(arguments[1]))
					prev_action.append((order, arg))
				else:
					prev_action.append((order, arguments))

			find = False
			for goal in self.__available_goals:
				if goal.getId() == id_objectif:
					find = True
					path = self.__getOrderTrajectoire(goal, elem_goal_id, position_depart_speciale)
					if path != []:
						self.__addGoal(path, goal, elem_goal_id, prev_action=prev_action)
					else:
						self.__logger.info(str(self.__robot_name) + " Aucun chemin disponible vers " +str(goal.getElemGoal(elem_goal_id).getPositionAndAngle())+" pour le goal d'id: " + str(id_objectif))
					break

			if not find:
				self.__logger.error(str(self.__robot_name) + " impossible de lui ajouter le goal d'id: " + str(id_objectif))
	
	def __getOrderTrajectoire(self, goal, elem_goal_id, position_depart_speciale=None):
		"""Il faut mettre à jour les polygones avant d'utiliser cette fonction"""
		if position_depart_speciale is not None:
			position_last_goal = position_depart_speciale
			self.__logger.debug("Position from position_depart_speciale" + str(position_last_goal))
		elif self.__blocked_goals:
			last_goal = self.__blocked_goals[-1]
			position_last_goal = last_goal.getElemGoalLocked().getPositionAndAngle()
			self.__logger.debug("Position from queue" + str(position_last_goal))
		else:
			position_last_goal = self.__data[self.__robot_name]["getPositionAndAngle"]
			self.__logger.debug("Position from data" + str(position_last_goal))

		position_to_reach = goal.getElemGoal(elem_goal_id).getPositionAndAngle()
		path = self.__PathFinding.getPath((position_last_goal[0], position_last_goal[1]), (position_to_reach[0], position_to_reach[1]), enable_smooth=True)

		return path

	def __tupleTrajectoireToDeque(self, tuple_trajectoire_list):
		order_list = deque()
		for tuple in tuple_trajectoire_list:
			order_list.append(('A_GOTO', [tuple[0], tuple[1]]))
		return order_list