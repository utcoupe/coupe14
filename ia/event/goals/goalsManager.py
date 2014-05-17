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

from .goal import *
from .elemGoal import *
from .navigation import *
from .visio import *
from .goalsLibrary import *
from .goalsChoice import *

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

		self.__back_triangle_stack = deque()
		self.__front_triangle_stack = deque()

		self.__data = self.__SubProcessManager.getData()
		self.__our_color = self.__data["METADATA"]["getOurColor"]
		self.__PathFinding = PathFinding((self.__data["FLUSSMITTEL"], self.__data["TIBOT"], self.__data["BIGENEMYBOT"], self.__data["SMALLENEMYBOT"]))

		self.__loadElemScript(base_dir+"/elemScripts.xml")
		self.__loadGoals(base_dir+"/goals.xml")

		self.__goalsLib = GoalsLibrary(self.__robot_name, self.__data, self.__blocked_goals, self.__PathFinding)
		self.__goalsChoice = GoalsChoice(self.__robot_name, self.__data, self.__goalsLib, self.__our_color, self.__back_triangle_stack, self.__front_triangle_stack)


		# Pour tester le déplacement du robot dans le simu lorsqu'il ne peut pas attraper un triangle
		if TEST_MODE == True:
			self.__hack_camera_simu_angle = 0
			self.__hack_camera_simu_x = 0
			self.__hack_camera_simu_y = 0

		#Permet de faire une symétrie pour les ordres dans le cas où on commence en jaune
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

		self.__reverse_table[(11,0)]=(12,0)
		self.__reverse_table[(11,1)]=(12,1)
		self.__reverse_table[(12,0)]=(11,0)
		self.__reverse_table[(12,1)]=(11,1)

		self.__reverse_table[(13,0)]=(13,1)
		self.__reverse_table[(13,1)]=(13,0)

		if self.__robot_name == "FLUSSMITTEL" and TEST_MODE == False:
			self.__vision = Visio('../supervisio/visio', 0, '../config/visio/visio_robot/', self.__data["FLUSSMITTEL"], True)
			self.__last_camera_color = None

		self.__loadBeginScript()

	def restartObjectifSearch(self):
		self.__queueBestGoals()

	def __queueBestGoals(self):
		if not self.__blocked_goals:
			self.__logger.debug(str(self.__robot_name)+" Recherche d'un nouvel objectif")	
			self.__PathFinding.update(self.__data[self.__robot_name])

			#On cherche l'elem goal le plus proche par bruteforce
			if self.__available_goals:
				best_goal = self.__goalsChoice.getBestGoal(self.__available_goals) #best_goal type (path, goal, id_elem_goal)

				if best_goal[1] != None:
					self.__logger.info("On a choisi l'objectif goal_id "+str(best_goal[1].getId())+" elem_goal_id "+str(best_goal[2])+" avec le path "+str(best_goal[0]))
					self.__SubProcessManager.setLastDateNoGoal(None)
					self.__addGoal(best_goal[0], best_goal[1], best_goal[2])
				else:
					self.__SubProcessManager.setLastDateNoGoal(int(time.time()*1000))
					self.__logger.info(str(self.__robot_name)+" aucun objectif accessible")
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
				self.__manageStepOver(objectif, id_objectif, skip_get_triangle=False)
				break

	def goalDynamiqueFinishedId(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__blocked_goals.remove(objectif)
				self.__dynamique_finished_goals.append(objectif)
				self.__logger.info(str(self.__robot_name)+" L'objectif "+str(objectif.getName())+" d'id "+str(objectif.getId())+" est a terminé ses actions dynamiques")
				self.__queueBestGoals()
				break

	def goalCanceledIdFromEvent(self, id_objectif):
		for objectif in self.__blocked_goals:
			if objectif.getId() == id_objectif:
				self.__cancelGoal(objectif, True)
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
			orders.extend(self.__goalsLib.tupleTrajectoireToDeque(tuple_trajectoire_list[1:]))
			orders.append( ("A_ROT", (goal.getElemGoalOfId(elem_goal_id).getPositionAndAngle()[2],)) )
			#on ajoute attend d'être arrivé pour lancer les actions
			orders.append( ("THEN", ()) )
			
			first_action_elem = goal.getElemGoalLocked().getFirstElemAction()
			orders.extend(first_action_elem)
			goal.getElemGoalLocked().removeFirstElemAction()

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

	def __cancelGoal(self, goal, fromEvent=False):
		self.__blocked_goals.remove(goal)#On ne peut pas enlever les ordres dans self.__dynamique_finished_goals
		self.__available_goals.append(goal)
		self.__logger.info('Goal ' + goal.getName() + ' has been canceled and is now released')
		self.__removeLastValueOfDeque(self.__id_objectif_send, goal.getId())
		goal.getElemGoalLocked().resetElemAction()

		if not fromEvent:
			self.__SubProcessManager.sendDeleteGoal(goal.getId())
		self.__queueBestGoals()


	def __finishGoal(self, goal):
		if goal in self.__dynamique_finished_goals:	
			self.__dynamique_finished_goals.remove(goal)
			self.__finished_goals.append(goal)
			if goal.getType() == "STORE_TRIANGLE":
				self.__front_triangle_stack.clear()
				self.__back_triangle_stack.clear()
			self.__logger.info('Goal ' + str(goal.getName()) + " d'id "+str(goal.getId())+" is finished")
			#Dans le cas où on aurait oublier le DYNAMIQUE_OVER
			self.__queueBestGoals()
		#Dans le cas où c'est l'autre robot qui à fait l'objectif
		elif goal in self.__available_goals:
			self.__available_goals.remove(goal)
			self.__finished_goals.append(goal)

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

		self.__removeLastValueOfDeque(self.__id_objectif_send, goal.getId())
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
			self.__logger.warning("Impossible de supprimer la valeur "+str(value_to_remove)+" de la liste "+str(deque))


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
							self.__cancelGoal(objectif, False)

					else:
						if (nb_front_stack < MAX_FRONT_TRIANGLE_STACK) and (nb_back_stack < MAX_BACK_TRIANGLE_STACK):
							self.__back_triangle_stack.append(self.__last_camera_color)
							position = -1
							hauteur = GARDE_AU_SOL + nb_front_stack*HAUTEUR_TRIANGLE + MARGE_DROP_TRIANGLE #ici c'est bien nb_front_stack !
						elif (nb_front_stack < MAX_FRONT_TRIANGLE_STACK) and (nb_back_stack >= MAX_BACK_TRIANGLE_STACK):
							self.__back_triangle_stack.popleft()
							script_to_send.append( ("O_RET", ()) )
							self.__back_triangle_stack.append(self.__last_camera_color)
							position = -1
							hauteur = GARDE_AU_SOL + nb_front_stack*HAUTEUR_TRIANGLE + MARGE_DROP_TRIANGLE #ici c'est bien nb_front_stack !
						else:
							self.__logger.error("On a pas la place pour stocker ce triangle ni à l'avant ni à l'arrière, ce cas ne devrait pas arriver !")
							stack_full = True
							self.__cancelGoal(objectif, False)

					if not stack_full:
						script_base = action_list
						for action in script_base:
							if action[0] == "STORE_TRIANGLE_IA":
								script_to_send.append( ("O_STORE_TRIANGLE", (int(position*hauteur),)) )
							elif action[0] == "GET_TRIANGLE_IA":
								pass
							else:
								script_to_send.append(action)
						self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), script_to_send)
						objectif.getElemGoalLocked().removeFirstElemAction()

				else:
					if TEST_MODE == False:
						limite_essai_viso = 5
						triangle_find = False
						triangle_list = []
						while limite_essai_viso != 0 and triangle_find == False:
							limite_essai_viso -= 1
							self.__vision.update()
							triangle_list = self.__vision.getTriangles()
							if triangle_list != []:
								triangle_find = True
								break
					else:
						triangle_find = True

					if triangle_find == False:
						self.__logger.warning("On a pas vu de triangle à la position attendu, dont on va supprimer l'objectif "+str(id_objectif))
						self.__last_camera_color = None
						self.__deleteGoal(objectif)
					else:
						if TEST_MODE == False:
							min_distance = float("inf")
							min_id = None
							for i, triangle in enumerate(triangle_list):
								distance = sqrt((triangle.coord[0]-220)**2 + (triangle.coord[1])**2)
								if distance < min_distance:
									min_distance = distance
									min_id = i
							triangle = triangle_list[i] 
							data_camera = (triangle.color, triangle.coord[0], triangle.coord[1]) #type (color, x, y)
						else:
							# Coordonées du triangle par rapport au centre du robot
							# sera corrigé par l'algo lors de la prise du premier triangle normalement
							temp = (220, -100)
							# Correction x y
							temp_x = temp[0] + self.__hack_camera_simu_x
							temp_y = temp[1] + self.__hack_camera_simu_y
							# Rotation du robot
							temp_x_rot = temp_x * cos(self.__hack_camera_simu_angle) - temp_y * sin(self.__hack_camera_simu_angle)
							temp_y_rot = temp_x * sin(self.__hack_camera_simu_angle) + temp_y * cos(self.__hack_camera_simu_angle)
							
							data_camera = ("RED", temp_x_rot, temp_y_rot)


						self.__last_camera_color = data_camera[0]
						#si on a la possibilité de le stocker
						if len(self.__front_triangle_stack)  >= MAX_FRONT_TRIANGLE_STACK:
							self.__logger.warning("Impossible de stocker ce triangle dans le robot, la pile de devant est pleine.")
							#Si besoin, on change la couleur du triangle pour la prochaine fois
							if self.__last_camera_color != objectif.getColorElemLock():
								objectif.switchColor()
							self.__cancelGoal(objectif, False)
						else:
							if self.__positionReady(data_camera[1], data_camera[2]):
								script_get_triangle = deque()
								script_get_triangle.append( ("O_GET_TRIANGLE", (data_camera[1], data_camera[2], HAUTEUR_TORCHE+3*HAUTEUR_TRIANGLE)) ) #TODO hauteur par triangle dans le cas des triangles au sol
								script_get_triangle.append( ("THEN", ()) )
								script_get_triangle.append( ("O_GET_BRAS_STATUS", ()) )
								script_get_triangle.append( ("THEN", (),) )
								self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), script_get_triangle)
							else:
								coord_to_move_to = self.__getPosToHaveTriangle(data_camera[1], data_camera[2])
								if coord_to_move_to != None:
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
										self.__PathFinding.update(self.__data[self.__robot_name])
										path = self.__PathFinding.getPath((x_abs, y_abs), (x+x_abs, y+y_abs), enable_smooth=True)
										if len(path) == 2:
											script_get_triangle.append( ("A_GOTOA", (path[1][0], path[1][1], a+a_abs)) ) 
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
										script_get_triangle.append( ("STEP_OVER", (),) )
										self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), script_get_triangle)
								else:
									self.__logger.warning("Impossible d'attendre le triangle d'après Alexis, data_camera: "+str(data_camera))
									self.__deleteGoal(objectif)
			
			#Si ce sont des actions simples, on ne devrait pas utliser STEP_OVER pour ça, mais plutôt THEN		
			else:
				self.__logger.warning("Attention, les actons sont simples, action_list "+str(action_list)+" on ne devrait pas utliser STEP_OVER pour ça, mais plutôt THEN")
				self.__SubProcessManager.sendGoalStepOver(objectif.getId(), objectif.getId(), action_list)
				objectif.getElemGoalLocked().removeFirstElemAction()
		else:
			self.__logger.warning("Pb, Il y a un STEP_OVER directement suivit d'un END ?")

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
				self.__manageStepOver(objectif, id_objectif, skip_get_triangle=True)
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
					
					goal.appendElemGoal( ElemGoal(id, x_objectif+x_elem, y_objectif+y_elem, angle_objectif+angle, points, priority, duration, color, self.__elem_script[id_script]) )

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
	

