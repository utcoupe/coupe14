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
from math import *
import time

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR,".."))

from .goal import *
from .elemGoal import *
from .navigation import *
from .visio import *
from .goalsLibrary import *
from .goalsChoice import *
from collision import *


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
		self.__id_objectif_send = deque()

		# FLUSSMITTEL
		self.__back_triangle_stack = deque()
		self.__front_triangle_stack = deque()
		# TIBOT

		self.__data = self.__SubProcessManager.getData()
		self.__our_color = self.__data["METADATA"]["getOurColor"]
		if self.__robot_name == "FLUSSMITTEL":
			self.__PathFinding = PathFinding((self.__data["FLUSSMITTEL"], self.__data["TIBOT"], self.__data["BIGENEMYBOT"], self.__data["SMALLENEMYBOT"]))
		else:
			self.__PathFinding = PathFinding((self.__data["TIBOT"], self.__data["FLUSSMITTEL"], self.__data["BIGENEMYBOT"], self.__data["SMALLENEMYBOT"]))

		
		self.__loadElemScript(base_dir+"/elemScripts.xml")
		self.__loadGoals(base_dir+"/goals.xml")

		self.__Collision = Collision(self.__data["FLUSSMITTEL"], self.__data["TIBOT"], self.__data["BIGENEMYBOT"], self.__data["SMALLENEMYBOT"])
		self.__goalsLib = GoalsLibrary(self.__robot_name, self.__data, self.__blocked_goals, self.__PathFinding)
		self.__goalsChoice = GoalsChoice(self.__robot_name, self.__data, self.__goalsLib, self.__Collision, self.__our_color, self.__back_triangle_stack, self.__front_triangle_stack, self.__available_goals, self.__finished_goals)

		self.__tibot_ready_for_filet = False
		temp = ("BIGENEMYBOT", "SMALLENEMYBOT", "FLUSSMITTEL", "TIBOT")
		self.__robot_to_check_goal_collision = []
		self.__last_enemy_pos = {}
		for robot in temp:
			if self.__data[robot] is not None:
				self.__robot_to_check_goal_collision.append(robot)
				self.__last_enemy_pos[robot] = None
		

		# Pour tester le déplacement du robot dans le simu lorsqu'il ne peut pas attraper un triangle
		if TEST_MODE == True:
			self.__hack_camera_simu_angle = 0
			self.__hack_camera_simu_x = 0
			self.__hack_camera_simu_y = 0

		if self.__robot_name == "FLUSSMITTEL" and TEST_MODE == False:
			self.__vision = Visio('../supervisio/visio', 0, '../config/visio/visio_robot/', self.__data["FLUSSMITTEL"], True)
		self.__last_camera_color = None
		self.__last_data_camera = None

		self.__loadBeginScript()


	def restartObjectifSearch(self):
		self.__queueBestGoals()

	def __queueBestGoals(self):
		if not self.__blocked_goals:
			self.__logger.debug(str(self.__robot_name)+" Recherche d'un nouvel objectif")	
			self.__PathFinding.update()

			#On cherche l'elem goal le plus proche par bruteforce
			if self.__available_goals:
				best_goal = self.__goalsChoice.getBestGoal(self. __tibot_ready_for_filet) #best_goal type (path, goal, id_elem_goal)

				if best_goal[1] != None:

					if self. __tibot_ready_for_filet == True:
						self.__logger.info("Finalement, on va refaire un objectif avant le filet")
						for goal_temp in self.__finished_goals:
							if goal_temp.getType() == "FILET":
								self.__finished_goals.remove(goal_temp)
								self.__available_goals.append(goal_temp)
								break
						self. __tibot_ready_for_filet = False

					self.__logger.info("On a choisi l'objectif "+str(best_goal[1].getName())+" goal_id "+str(best_goal[1].getId())+" elem_goal_id "+str(best_goal[2])+" avec le path "+str(best_goal[0]))
					self.__SubProcessManager.setLastDateNoGoal(None)
					self.__addGoal(best_goal[0], best_goal[1], best_goal[2])
				else:
					self.__SubProcessManager.setLastDateNoGoal(int(time.time()*1000))
					self.__logger.info(str(self.__robot_name)+" aucun objectifs accessibles")
			else:
				self.__logger.info(str(self.__robot_name)+" N'a plus aucun objectif disponible, GG (ou pas, y'a toujours un truc à faire) !")


	#GOAL management from ID
	def blockGoalFromId(self, id_objectif):
		"""utilisé uniquement quand un autre objectif manager block un goal"""
		#osef, il n'y aura pas d'intersection sur les objectifs !
		pass

	def goalStepOverId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__manageStepOver(objectif, id_objectif)
				break

	def goalDynamiqueFinishedId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__blocked_goals.remove(objectif)
				self.__dynamique_finished_goals.append(objectif)

				if objectif.getType() == "STORE_TRIANGLE":
					self.__front_triangle_stack.clear()
					self.__back_triangle_stack.clear()

				self.__logger.info(str(self.__robot_name)+" L'objectif "+str(objectif.getName())+" d'id "+str(objectif.getId())+" a terminé ses actions dynamiques")
				self.__queueBestGoals()
				break

	def goalCanceledIdFromEvent(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__cancelGoal(objectif, fromEvent = True)
				break

	def goalFinishedId(self, id_objectif):
		for objectif in self.__dynamique_finished_goals:
			if objectif.getId() == id_objectif:
				self.__finishGoal(objectif)
		#Dans le cas où c'est l'autre subprocess qui fait l'objectif 
		for objectif in self.__available_goals:
			if objectif.getId() == id_objectif:
				self.__finishGoal(objectif) 

	#GOAL management from GOAL
	def __tryBlockGoal(self, goal, elem_goal_id):
		if goal in self.__available_goals:
			self.__available_goals.remove(goal)
			self.__blocked_goals.append(goal)
			goal.setElemGoalLocked(goal.getElemGoalOfId(elem_goal_id))
			self.__logger.info(str(self.__robot_name)+' Goal '+goal.getName()+' id: '+str(goal.getId())+" elem_goal_id "+str(elem_goal_id)+' is blocked')
			return True
		else:
			self.__logger.warning(str(self.__robot_name)+' Goal '+goal.getName()+' id: '+str(goal.getId())+" elem_goal_id "+str(elem_goal_id)+" n'a pas pu être bloqué")
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
			orders.extend(self.__goalsLib.tupleTrajectoireToDeque(tuple_trajectoire_list[1:]))
			orders.append( ("A_ROT", (goal.getElemGoalOfId(elem_goal_id).getPositionAndAngle()[2],)) )
			#on ajoute attend d'être arrivé pour lancer les actions
			orders.append( ("THEN", ()) )
			
			first_action_elem = goal.getFirstElemAction()

			#Hack pour le cas des torches qui sont des actions qu'on peut faire en plusieurs fois
			if first_action_elem:
				if first_action_elem[0][0] == "GET_TRIANGLE_IA_TORCHE" or first_action_elem[0][0] == "GET_TRIANGLE_IA" or first_action_elem[0][0] == "GET_TRIANGLE_IA_TORCHE_SCRIPT":
					orders.append( ("STEP_OVER", ()) )
				else:
					orders.extend(first_action_elem)
					goal.removeFirstElemAction()

			#on envoi le tout
			if self.__id_objectif_send:
				prev_id = self.__id_objectif_send[-1]
			else:
				prev_id = None
			self.__SubProcessManager.sendGoal(prev_id, goal.getId(), orders)
			self.__id_objectif_send.append(goal.getId())
		else:
			#TODO, ce cas peut-il vrament arrivé ?
			self.__logger.error("On va rechercher un nouvel ordre, ce cas peut-il vrament arrivé")
			self.__queueBestGoals()

	def __cancelGoal(self, goal, fromEvent = False):
		self.__blocked_goals.remove(goal)#On ne peut pas enlever les ordres dans self.__dynamique_finished_goals
		self.__available_goals.append(goal)
		self.__logger.info('Goal ' + goal.getName() + ' has been canceled and is now released')
		self.__removeLastValueOfDeque(self.__id_objectif_send, goal.getId())
		#On ne reset pas les torches, comme ça on sait combien de triangle on doit en extraire
		if goal.getType() != "TORCHE":
			goal.resetElemAction()

		if not fromEvent:
			self.__SubProcessManager.sendDeleteGoal(goal.getId())
		self.__queueBestGoals()


	def __finishGoal(self, goal):
		if goal in self.__dynamique_finished_goals:	
			self.__dynamique_finished_goals.remove(goal)
			self.__finished_goals.append(goal)
			self.__logger.info('Goal ' + str(goal.getName()) + " d'id "+str(goal.getId())+" is finished")
			if goal.getType() == "FILET":
				#on reset pour pouvoir retirer un filet
				goal.resetElemAction()
				self.__tibot_ready_for_filet = True
				self.__logger.info("Tibot est en position pour tirer le filet.")
			#Dans le cas où on aurait oublier le DYNAMIQUE_OVER
			self.__queueBestGoals()
		
		#Dans le cas où c'est l'autre robot qui à fait l'objectif
		elif goal in self.__available_goals:
			self.__available_goals.remove(goal)
			self.__finished_goals.append(goal)

	def goalDeletedIdFromEvent(self, id_to_delete):
		for goal in (self.__available_goals + self.__blocked_goals + self.__dynamique_finished_goals + self.__finished_goals):
			if goal.getId() == id_to_delete:
				self.__deleteGoal(goal, fromEvent = True)


	def __deleteGoal(self, goal, fromEvent = False, fromGoalCollision=False):
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
		if fromGoalCollision == False:
			self.__removeLastValueOfDeque(self.__id_objectif_send, goal.getId())
		if fromEvent == False and fromGoalCollision == False:
			self.__SubProcessManager.sendDeleteGoal(goal.getId())
		if success:
			self.__logger.info('Goal ' + goal.getName() + ' is delete')
		else:
			self.__logger.error('Goal ' + goal.getName() + " can't be delete")
		self.__queueBestGoals()


	def __removeLastValueOfDeque(self, deque_list, value_to_remove):
		removed_deque = deque()
		find = False

		while deque_list:
			temp_value = deque_list.pop()
			if temp_value == value_to_remove:
				find = True
				deque_list.extend(removed_deque)
				break
			else:
				removed_deque.appendleft(temp_value)

		if find == True:
			self.__logger.debug("On supprime la dernière occurance de "+str(value_to_remove)+" il reste "+str(deque_list))
		else:
			deque_list.extend(removed_deque)
			self.__logger.warning("Impossible de supprimer la valeur "+str(value_to_remove)+" de la liste "+str(deque_list))

	def __manageStepBras(self, objectif, id_objectif):
		action_list = objectif.getFirstElemAction()
		if not action_list:
			self.__logger.warning("Pb, Il y a un STEP_OVER directement suivit d'un END ?")
			return None

		objectif.getElemGoalLocked().setCoordBrasVerified(True)

		if (action_list[0][0] == "GET_TRIANGLE_IA" or action_list[0][0] == "GET_TRIANGLE_IA_TORCHE" or action_list[0][0] == "GET_TRIANGLE_IA_TORCHE_SCRIPT"):
			can_be_store, position, hauteur_drop, script_to_send = self.__last_data_camera

			if not can_be_store:
				self.__logger.info("Impossible de stocker le triangle, ca cas ne devrait pas arriver, si ?")
				self.__cancelGoal(objectif, False)
				return None

			if script_to_send:
				self.__back_triangle_stack.popleft()
			if position == 1:
				self.__front_triangle_stack.append(self.__last_camera_color)
			else:
				self.__back_triangle_stack.append(self.__last_camera_color)
			script_base = action_list
			for action in script_base:
				if action[0] == "STORE_TRIANGLE_IA":
					script_to_send.append( ("O_STORE_TRIANGLE", (int(position*hauteur_drop),)) )
					if objectif.getType() != "TORCHE" and position == -1:
						script_to_send.append( ("THEN", ()) )
						script_to_send.append( ("O_RET", ()) )
				elif action[0] == "GET_TRIANGLE_IA" or action[0] == "GET_TRIANGLE_IA_TORCHE" or action[0] == "GET_TRIANGLE_IA_TORCHE_SCRIPT":
					pass
				else:
					script_to_send.append(action)
			self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), script_to_send)
			objectif.removeFirstElemAction()
		#Si ce sont des actions simples, on ne devrait pas utliser STEP_OVER pour ça, mais plutôt THEN		
		else:
			self.__logger.warning("Attention, les actions sont simples, action_list "+str(action_list)+" on ne devrait pas utliser STEP_OVER pour ça, mais plutôt THEN")
			self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), action_list)
			objectif.removeFirstElemAction()
	

	def __manageStepOver(self, objectif, id_objectif):
		action_list = objectif.getFirstElemAction()
		if not action_list:
			self.__logger.warning("Pb, Il y a un STEP_OVER directement suivit d'un END ?")
			return None

		#Si ce sont des actions simples, on ne devrait pas utliser STEP_OVER pour ça, mais plutôt THEN
		if action_list[0][0] != "GET_TRIANGLE_IA" and action_list[0][0] != "GET_TRIANGLE_IA_TORCHE" and action_list[0][0] != "GET_TRIANGLE_IA_TORCHE_SCRIPT":
			self.__logger.warning("Attention, les actions sont simples, action_list "+str(action_list)+" on ne devrait pas utliser STEP_OVER pour ça, mais plutôt THEN")
			self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), action_list)
			objectif.removeFirstElemAction()
			return None

		get_triangle_mode = action_list[0][0]
		if get_triangle_mode != "GET_TRIANGLE_IA_TORCHE_SCRIPT":
			data_camera = self.__getVisioData(objectif)
			if data_camera == None:
				self.__logger.info("On a pas trouvé de données camera pour l'objectif d'id "+str(objectif.getType()))
				return None

			#Si besoin, on change la couleur du triangle pour la prochaine fois
			if data_camera[0] != objectif.getColorElemLock():
				objectif.switchColor()

			#Si ce n'est pas une torche et que la couleur est déjà bonne
			if data_camera[0] == self.__our_color and objectif.getType() != "TORCHE":
				self.__logger.info("Ce triangle est de notre couleur donc on le laisse ici")
				self.__deleteGoal(objectif)
				return None

			can_be_store, position, hauteur_drop, script_data_to_get = self.__howToStoreTriangle(data_camera[0])
		else:
			color_temp = objectif.getColorForScriptTorche()
			if color_temp == 1:
				triangle_color = self.__our_color
			elif color_temp == 0:
				if self.__our_color == "RED":
					triangle_color = "YELLOW"
				else:
					triangle_color = "RED"
			else:
				triangle_color = self.__our_color# pour eviter le plantage
				self.__logger("Erreur de couleur dans le script torche")
			can_be_store, position, hauteur_drop, script_data_to_get = self.__howToStoreTriangle(triangle_color)
			abs_coord = objectif.getPosition()
			relative_coord = self.__goalsLib.calcArmPos(abs_coord[0], abs_coord[1])
			data_camera = ("FUCK", relative_coord[0], relative_coord[1])
		self.__last_data_camera =  (can_be_store, position, hauteur_drop, script_data_to_get)
		#si on a la possibilité de le stocker
		if not can_be_store:
			self.__logger.info("Impossible de stocker le triangle de couleur "+str(data_camera[0])+" self.__front_triangle_stack "+str(self.__front_triangle_stack)+" self.__back_triangle_stack "+str(self.__back_triangle_stack))
			self.__cancelGoal(objectif, False)
			return None
			
		#if self.__positionReady(data_camera[1], data_camera[2]):
		if True:
			script_get_triangle = deque()
			if get_triangle_mode == "GET_TRIANGLE_IA":
				script_get_triangle.append( ("O_GET_TRIANGLE", (data_camera[1], data_camera[2], HAUTEUR_TRIANGLE)) )
			elif get_triangle_mode == "GET_TRIANGLE_IA_TORCHE":
				#Si on en a déjà pris un avec succes
				last_coord = objectif.getElemGoalLocked().getCoordBras()
				if last_coord is not None and objectif.getElemGoalLocked().getCoordBrasVerified():
					script_get_triangle.append( ("O_GET_TRIANGLE", (last_coord[0], last_coord[1], HAUTEUR_TORCHE+3*HAUTEUR_TRIANGLE)) )
				else:
					objectif.getElemGoalLocked().setCoordBras(data_camera[1], data_camera[2])
					objectif.getElemGoalLocked().setCoordBrasVerified(False)
					script_get_triangle.append( ("O_GET_TRIANGLE", (data_camera[1], data_camera[2], HAUTEUR_TORCHE+3*HAUTEUR_TRIANGLE)) )
			elif get_triangle_mode == "GET_TRIANGLE_IA_TORCHE_SCRIPT":
				script_get_triangle.append( ("O_GET_TRIANGLE", (relative_coord[0], relative_coord[1], HAUTEUR_TORCHE+3*HAUTEUR_TRIANGLE)) )
				
			script_get_triangle.append( ("THEN", ()) )
			script_get_triangle.append( ("O_GET_BRAS_STATUS", ()) )
			script_get_triangle.append( ("THEN", (),) )
			self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), script_get_triangle)
		else:
			coord_to_move_to = self.__getPosToHaveTriangle(data_camera[1], data_camera[2])
			if coord_to_move_to == None:
				self.__logger.warning("Impossible d'attendre le triangle d'après Alexis, data_camera: "+str(data_camera))
				self.__deleteGoal(objectif)
				return None
			find  = True
			x, y, a = coord_to_move_to
			x_abs, y_abs, a_abs = self.__data[self.__robot_name]["getPositionAndAngle"]
			script_get_triangle = deque()

			if TEST_MODE == True:
				self.__hack_camera_simu_x -= x
				self.__hack_camera_simu_y -= y
				self.__hack_camera_simu_angle -= a

			# Si on a besoin d'avancer, on vérifie avec le pathfinding
			if x != 0 or y != 0:
				self.__PathFinding.update()
				path = self.__PathFinding.getPath((x_abs, y_abs), (x+x_abs, y+y_abs), enable_smooth=True)
				if len(path) == 2:
					script_get_triangle.append( ("A_GOTOA", (path[1][0], path[1][1], a+a_abs)) ) 
					script_get_triangle.append( ("THEN", (),) )
					script_get_triangle.append( ("STEP_OVER", (),) )
					self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), script_get_triangle)
				elif len(path) > 2:
					self.__logger.warning("Impossible d'attendre le triangle en ligne droite d'après PathFinding, data_camera: "+str(data_camera)+" path: "+str(path)+" x+x_abs: "+str(x+x_abs)+" y+y_abs "+str(y+y_abs)+" a+a_abs "+str(a+a_abs))
					self.__deleteGoal(objectif)
				else:
					self.__logger.warning("Impossible d'attendre le triangle d'après PathFinding, data_camera: "+str(data_camera)+" path: "+str(path)+" x+x_abs: "+str(x+x_abs)+" y+y_abs "+str(y+y_abs)+" a+a_abs "+str(a+a_abs))
					self.__deleteGoal(objectif)
			# Sinon on a besoin de juste tourner
			else:
				script_get_triangle.append( ("A_ROT", (a+a_abs,)) ) 
				script_get_triangle.append( ("THEN", (),) )
				script_get_triangle.append( ("STEP_OVER", (),) )
				self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), script_get_triangle)

	def __howToStoreTriangle(self, color): #return type: (can_be_store, position, hauteur_drop)
		position = None
		hauteur_drop = None
		nb_front_stack = len(self.__front_triangle_stack) 
		nb_back_stack = len(self.__back_triangle_stack)
		can_be_store = True
		script_to_send = deque()

		if self.__our_color == color:
			if nb_front_stack < MAX_FRONT_TRIANGLE_STACK_STORE:
				position = 1
				hauteur_drop = GARDE_AU_SOL + nb_front_stack*HAUTEUR_TRIANGLE + MARGE_DROP_TRIANGLE
			else:
				self.__logger.warning("On a plus de place à l'avant pour stocker ce triangle.")
				can_be_store = False

		else:
			if (nb_front_stack < MAX_FRONT_TRIANGLE_STACK) and (nb_back_stack < MAX_BACK_TRIANGLE_STACK):
				position = -1
				hauteur_drop = GARDE_AU_SOL + nb_front_stack*HAUTEUR_TRIANGLE + MARGE_DROP_TRIANGLE #ici c'est bien nb_front_stack !
			elif (nb_front_stack < MAX_FRONT_TRIANGLE_STACK) and (nb_back_stack >= MAX_BACK_TRIANGLE_STACK):
				script_to_send.append( ("O_RET", ()) )
				position = -1
				hauteur_drop = GARDE_AU_SOL + nb_front_stack*HAUTEUR_TRIANGLE + MARGE_DROP_TRIANGLE #ici c'est bien nb_front_stack !
			else:
				self.__logger.warning("On a plus la place pour stocker ce triangle, ni à l'avant ni à l'arrière.")
				can_be_store = False

		return (can_be_store, position, hauteur_drop, script_to_send)
	
	def __getVisioData(self, objectif):
		if TEST_MODE == False:
			limite_essai_viso = NB_VISIO_TRY
			list_of_triangle_list = []
			triangle_list_temp = []
			time.sleep(0.1)
			while limite_essai_viso > 0 and len(list_of_triangle_list) < NB_VISIO_DATA_NEEDED:
				limite_essai_viso -= 1
				time.sleep(0.05)
				self.__vision.update(objectif.getType() == "TORCHE")
				triangle_list_temp = self.__vision.getTriangles()
				if triangle_list_temp != []:
					list_of_triangle_list.append(triangle_list_temp)

			if len(list_of_triangle_list) >= NB_VISIO_DATA_NEEDED:
				data_camera = self.__getBestDataTriangleOfList(list_of_triangle_list)
				if data_camera == None:
					self.__last_camera_color = None
					self.__deleteGoal(objectif)
			else:
				self.__logger.warning("On a pas vu de triangle à la position attendu, list_of_triangle_list "+str(list_of_triangle_list)+" dont on va supprimer l'objectif d'id "+str(objectif.getId()))
				self.__last_camera_color = None
				data_camera = None
				self.__deleteGoal(objectif)
				

		else:
			# Coordonées du triangle par rapport au centre du robot
			# sera corrigé par l'algo lors de la prise du premier triangle normalement
			temp = (220, 0)
			# Correction x y
			temp_x = temp[0] + self.__hack_camera_simu_x
			temp_y = temp[1] + self.__hack_camera_simu_y
			# Rotation du robot
			temp_x_rot = temp_x * cos(self.__hack_camera_simu_angle) - temp_y * sin(self.__hack_camera_simu_angle)
			temp_y_rot = temp_x * sin(self.__hack_camera_simu_angle) + temp_y * cos(self.__hack_camera_simu_angle)
			
			data_camera = ("RED", temp_x_rot, temp_y_rot)

		return data_camera #type (color, x, y)

	

	def __getBestDataTriangleOfList(self, list_of_triangle_list):
		#On prend le meilleur de chaque listes
		list_of_best_triangle = []
		for triangle_list in list_of_triangle_list:
			min_distance = float("inf")
			min_id = None
			for i, triangle in enumerate(triangle_list):
				if self.__isThisTriangleOnTable(triangle):
					distance = sqrt((triangle.coord[0]-220)**2 + (triangle.coord[1])**2)
					if distance < min_distance and distance < VISIO_MAX_DIST_TRIANGLE:
						min_distance = distance
						min_id = i
			if min_id is not None:
				list_of_best_triangle.append(triangle_list[min_id])

		#On les comparent les un aux autres et on prend le plus proche des autres
		min_distance = float("inf")
		min_id = None
		for triangle in list_of_best_triangle:
			min_distance_temp = float("inf")
			min_id_temp = None
			for i, triangle_temp in enumerate(list_of_best_triangle):
				if triangle.color == triangle_temp.color:
					distance = sqrt((triangle_temp.coord[0] - triangle.coord[0])**2 + (triangle_temp.coord[1] - triangle.coord[1])**2)
					if distance < min_distance_temp:
						min_distance_temp = distance
						min_id_temp = i

			if min_distance_temp < min_distance:
				min_distance = min_distance_temp
				min_id = min_id_temp
		if min_id is not None:
			triangle_choisi = list_of_best_triangle[min_id]
			self.__logger.debug("On a choisi le triangle coord[0] "+str(triangle_choisi.coord[0])+" coord[1] "+str(triangle_choisi.coord[1])+" color "+str(triangle_choisi.color))
			return (triangle_choisi.color, triangle_choisi.coord[0], triangle_choisi.coord[1]) #type (color, x, y)
		else:
			self.__logger.warning("On a bien reçu assez de données viso, mais elles n'avaient aucun sens... list_of_best_triangle "+str(list_of_best_triangle))
			return None

	def __isThisTriangleOnTable(self, triangle):
		x, y, a = self.__data[self.__robot_name]["getPositionAndAngle"]
		x += (cos(a)*triangle.coord[0]) + (cos(a+1.57)*triangle.coord[1])
		y += (sin(a)+triangle.coord[0]) + (sin(a+1.57)+triangle.coord[1])

		if x<0 or x>3000 or y<0 or y>2000:
			self.__logger.warning("On a vu un triangle en dehors de la map, triangle "+str(triangle)+" our_bot "+str(self.__data[self.__robot_name]["getPositionAndAngle"])+" x "+str(x)+" y "+str(y))
			return False
		return True
		
	def __positionReady(self, x, y):
		x2 = x - CENTRE_BRAS_X
		y2 = y - CENTRE_BRAS_Y
		a, r = self.__toPolaire(x2, y2)
		return self.__positionReadyPolaire(a, r)

	def __positionReadyPolaire(self, a, r):
		if a >= ANGLE_MIN and a <= ANGLE_MAX:
			if r >= OUVERTURE_BRAS_MIN and r <= OUVERTURE_BRAS_MAX:
				return True
		return False

	def __toCartesien(self, a, r):
		return (r * cos(a), r * sin(a))
	def __toPolaire(self, x, y):
		return (atan2(y,x), hypot(x,y))

	# To verify
	def __getPosToHaveTriangle(self, x, y):
		# "Sécurité", peut être enlevé à priori
		"""
		if __positionReady(x, y):
			return 0
		"""
		# Variable à retourner en cartésien
		r_to_go = 0
		a_to_go = 0
		
		temp_x, temp_y = self.__toCartesien(ANGLE_MAX - ANGLE_MIN, OUVERTURE_BRAS_MAX - OUVERTURE_BRAS_MIN)
		centre_zone_x = temp_x + CENTRE_BRAS_X
		centre_zone_y = temp_y + CENTRE_BRAS_Y

		if hypot(x, y) > hypot(CENTRE_BRAS_Y, CENTRE_BRAS_X + OUVERTURE_BRAS_MAX) - MARGE_OUVERTURE_BRAS_MAX_DEPLACEMENT:
			# Il faut avancer
			a, r = self.__toPolaire(x, y)
			r_to_go = r - hypot(centre_zone_x, centre_zone_y)
			r -= r_to_go
			x, y = self.__toCartesien(a, r)

		elif hypot(x, y) < hypot(CENTRE_BRAS_Y, CENTRE_BRAS_X) + MARGE_OUVERTURE_BRAS_MIN_DEPLACEMENT:
			# Il faut reculer
			a, r = self.__toPolaire(x, y)
			r_to_go = hypot(centre_zone_x, centre_zone_y) - r
			r += r_to_go
			x, y = self.__toCartesien(a, r)

		# Angle en degrés entre deux calculs
		delta_a = 1

		# i_* => itérateurs
		i_x = x
		i_y = y

		somme_a = 0
		nb_a = 0
		stop = False

		for i in range(int(-90/delta_a),int(90/delta_a)): # to modify
			i_rot = radians(i*delta_a)
			i_x = x * cos(i_rot) - y * sin(i_rot)
			i_y = x * sin(i_rot) + y * cos(i_rot)
			if self.__positionReady(i_x, i_y):
				somme_a += i_rot
				nb_a += 1
				stop = True

			# On s'arrête si on a déjà trouvé des positions et qu'on en trouve plus,
			# pour ne pas que la moyenne tombe dans un "trou"
			elif stop == True:
				break

		if nb_a == 0:
			self.__logger.error("Fuck, impossible d'attraper le triangle !")
			return None
		else:
			# Un - car on fait tourner le point (x,y) et non le robot
			a_to_go = -somme_a / nb_a
			x_to_go, y_to_go = self.__toCartesien(a_to_go, r_to_go)
			#self.__logger.info("Nouvelle position pour attraper le triangle : ("+int(x_to_go)+','+int(y_to_go)+','+float(a_to_go)+')')
			return (int(x_to_go), int(y_to_go), float(a_to_go))

	def processBrasStatus(self, status_fin, id_objectif):
		objectif = None
		for objectif_temp in self.__blocked_goals:
			if objectif_temp.getId() == id_objectif:
				objectif = objectif_temp

		if objectif is None:
			self.__logger.critical("L'objectif a supprimer n'est plus dans la liste des bloqués "+str(id_objectif))
		else:
			if status_fin == 1:
				self.__manageStepBras(objectif, id_objectif)
			else:
				self.__logger.warning("La prehention du trianglé à échoué, donc on supprime l'ordre "+str(id_objectif))
				self.__deleteGoal(objectif)


	#TODO utiliser cette fonction ?
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
			x_objectif		= int(xml_goal.getElementsByTagName('x_objectif')[0].firstChild.nodeValue)
			y_objectif		= int(xml_goal.getElementsByTagName('y_objectif')[0].firstChild.nodeValue)
			angle_objectif	= float(xml_goal.getElementsByTagName('angle_objectif')[0].firstChild.nodeValue)

			#On ajoute uniquement les objectifs qui nous concerne
			if concerned_robot == "ALL" or concerned_robot == self.__robot_name:
				goal = Goal(id, name, type, concerned_robot, x_objectif, y_objectif)

				#Hack pour ignore le premier triangle que le petit fait tombé
				if (self.__our_color == "RED" and id == 0) or (self.__our_color == "YELLOW" and id == 1):
					self.__finished_goals.append(goal)
				#Hack pour ignorer le second mamouth
				#elif (self.__our_color == "RED" and id == 12) or (self.__our_color == "YELLOW" and id == 11):
					#self.__finished_goals.append(goal)
				else:
					self.__available_goals.append(goal)

				for elem_goal in xml_goal.getElementsByTagName('elem_goal'):
					id			= int(elem_goal.getElementsByTagName('id')[0].firstChild.nodeValue)
					x_elem		= int(elem_goal.getElementsByTagName('x_elem')[0].firstChild.nodeValue)
					y_elem		= int(elem_goal.getElementsByTagName('y_elem')[0].firstChild.nodeValue)
					angle		= float(elem_goal.getElementsByTagName('angle')[0].firstChild.nodeValue)
					points		= int(elem_goal.getElementsByTagName('points')[0].firstChild.nodeValue)
					priority	= int(elem_goal.getElementsByTagName('priority')[0].firstChild.nodeValue)
					duration	= int(elem_goal.getElementsByTagName('duration')[0].firstChild.nodeValue)
					color		= str(elem_goal.getElementsByTagName('color')[0].firstChild.nodeValue)
					script_only	= bool(elem_goal.getElementsByTagName('script_only')[0].firstChild.nodeValue)
					id_script	= int(elem_goal.getElementsByTagName('id_script')[0].firstChild.nodeValue)
					
					goal.appendElemGoal( ElemGoal(id, x_objectif+x_elem, y_objectif+y_elem, angle_objectif+angle, points, priority, duration, color, script_only, self.__elem_script[id_script]) )

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

		self.__PathFinding.update()

		for xml_goal in dom.getElementsByTagName('objectif'):
			id_objectif	= int(xml_goal.getElementsByTagName('id_objectif')[0].firstChild.nodeValue)
			elem_goal_id= int(xml_goal.getElementsByTagName('elem_goal_id')[0].firstChild.nodeValue)

			position_depart_speciale = None
			#Inversion du script
			if self.__our_color == "YELLOW":
				id_objectif, elem_goal_id = self.__goalsLib.reverseGoalId(id_objectif, elem_goal_id)
			prev_action = deque()
			for raw_prev_action in xml_goal.getElementsByTagName('prev_action'):
				raw_order = raw_prev_action.childNodes[0].nodeValue.split()
				order = str(raw_order[0])
				arguments = raw_order[1:]
				if order == "MYPOSITION_INFO":
					if self.__our_color == "RED":
						position_depart_speciale = (int(arguments[0]), int(arguments[1]))
					else:
						position_depart_speciale = (3000 - int(arguments[0]), int(arguments[1]))
				elif order == "O_BALAI" and self.__our_color == "YELLOW":
					arg = (int(arguments[0]) * -1,)
					prev_action.append((order, arg))
				elif order == "A_GOTO" and self.__our_color == "YELLOW":
					arg = (3000 - int(arguments[0]), int(arguments[1]))
					prev_action.append((order, arg))
				elif order == "A_GOTOA" and self.__our_color == "YELLOW":
					arg = (3000 - int(arguments[0]), int(arguments[1]), float(arguments[2])-1.57)
					prev_action.append((order, arg))
				else:
					prev_action.append((order, arguments))

			find = False
			for goal in self.__available_goals:
				if goal.getId() == id_objectif:
					find = True
					position_last_goal = self.__goalsLib.getPositionLastGoal(position_depart_speciale)
					path = self.__goalsLib.getOrderTrajectoire(goal, elem_goal_id, position_last_goal)
					if path != []:
						self.__addGoal(path, goal, elem_goal_id, prev_action=prev_action)
					else:
						self.__logger.info(str(self.__robot_name) + " Aucun chemin disponible vers " +str(goal.getElemGoalOfId(elem_goal_id).getPositionAndAngle())+" pour le goal d'id: " + str(id_objectif))
					break

			#Pour le cas où on ne peut lui ajouter aucun objectif
			self.__queueBestGoals()

			if not find:
				self.__logger.error(str(self.__robot_name) + " impossible de lui ajouter le goal d'id: " + str(id_objectif))
	
	def __check_goal_proximity(self,goal,bot):
		"""
		Vérifie si un robot adverse est passé sur un objectif.
		@param goal objectif qu'on regarde
		@param bot robot ennemi considéré
		"""
		pos_goal = goal.getPosition()
		pos_bot = bot["getPosition"]
		dist_bot = sqrt((pos_goal[0] - pos_bot[0])**2+(pos_goal[1] - pos_bot[1])**2)
		if dist_bot < bot["getRayon"]:
			return True
		else:
			return False

	def __check_goal_TS(self,goal,bot, robot):
		"""
		Vérifie si le robot est resté proche d'un goal pendant longtemps.
		@param goal objectif qu'on regarde
		@param bot robot ennemi considéré
		"""
		ts = self.__data["METADATA"]["getGameClock"] #timeStamp
		ts_goal = goal.getTSProximiy()

		pos_goal = goal.getPosition()
		pos_bot = bot["getPosition"]
		dist_bot = sqrt((pos_goal[0] - pos_bot[0])**2+(pos_goal[1] - pos_bot[1])**2)
		if dist_bot < bot["getRayon"]*1.5:
			if ts_goal == -1:
				goal.setTSProximiy(ts)
		elif ts_goal != -1:
			if ts - ts_goal > 6000:
				goal.setAlreadyDone(100)
				self.__logger.info("On supprime le goal d'id "+str(goal.getId())+" car "+str(robot)+" est resté longtemps à côté")
				self.__deleteGoal(goal, fromGoalCollision=True)
				goal.setTSProximiy(self.__data["METADATA"]["getGameClock"])
				goal.setTSProximiy(-1)
			else:
				goal.setTSProximiy(-1)

	def updateAlreadyDone(self):
		"""
		Met à jour le pourcentage de possibilité que le robot adverse ait accomplit un objectif
		"""
		#quand on t'appel check self.__data, dont data["BIGENEMYBOT"]["getPosition"], data["SMALLENEMYBOT"]["getPosition"], data["METADATA"]["getGameClock"]
		#pour tous les objectifs dans self.__available_goals, appel la fonction getAlreadyDone et setAlreadyDone
		if self.__data["METADATA"]["getGameClock"] is not None and self.__robot_name == "FLUSSMITTEL":
			for robot in self.__robot_to_check_goal_collision:
				if self.__last_enemy_pos[robot] != self.__data[robot]["getPosition"]:
					self.__last_enemy_pos[robot] = self.__data[robot]["getPosition"]
					for goal in self.__available_goals:
						if goal.getAlreadyDone() < 100:
							if self.__check_goal_proximity(goal, self.__data[robot]) is True:
								goal.setAlreadyDone(100)
								goal.setGoalDone(True)
								self.__logger.info("On supprime le goal d'id "+str(goal.getId())+" car "+str(robot)+" est passé dessus")
								self.__deleteGoal(goal, fromGoalCollision=True)
							else:
								self.__check_goal_TS(goal,self.__data[robot], robot)
