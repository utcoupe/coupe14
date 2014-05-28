# -*- coding: utf-8 -*-
"""
Class used to choose what to do
"""

import logging
from math import *

from .goal import *
from .elemGoal import *
from .navigation import *
from .goalsLibrary import *

class GoalsChoice:
	def __init__(self, robot_name, data, goalsLib, Collision, our_color, back_triangle_stack, front_triangle_stack, available_goals, finished_goals):
		self.__logger = logging.getLogger(__name__)

		self.__robot_name = robot_name
		self.__data = data
		self.__goalsLib = goalsLib
		self.__Collision = Collision
		self.__our_color = our_color
		self.__available_goals = available_goals
		self.__finished_goals = finished_goals

		# Variables FLUSSMITTEL
		self.__back_triangle_stack = back_triangle_stack
		self.__front_triangle_stack = front_triangle_stack

		# Priorité
		self.__triangles_gauche = [0,6,7,8,9]
		self.__torche_gauche = 17
		""" Ancien choix d'objectif
		self.__prio_FM_areas = ["STORE_TRIANGLE_GAUCHE", "STORE_TRIANGLE_CENTRE", "STORE_TRIANGLE_DROITE"]
		#self.__prio_FM_area_triangles = {"STORE_TRIANGLE_CENTRE": [7,17], "STORE_TRIANGLE_GAUCHE": [8,17,9,7,5], "STORE_TRIANGLE_DROITE": [7,17]}
		self.__prio_FM_area_triangles = {"STORE_TRIANGLE_CENTRE": [], "STORE_TRIANGLE_GAUCHE": [], "STORE_TRIANGLE_DROITE": []}
		if self.__our_color == "YELLOW":
			self.__prio_FM_areas = ["STORE_TRIANGLE_DROITE", "STORE_TRIANGLE_CENTRE", "STORE_TRIANGLE_GAUCHE"]
			self.__prio_FM_area_triangles["STORE_TRIANGLE_CENTRE"] = self.__goalsLib.reverseTabOfGoalId(self.__prio_FM_area_triangles["STORE_TRIANGLE_CENTRE"])
			temp = self.__goalsLib.reverseTabOfGoalId(self.__prio_FM_area_triangles["STORE_TRIANGLE_GAUCHE"])
			self.__prio_FM_area_triangles["STORE_TRIANGLE_GAUCHE"] = self.__goalsLib.reverseTabOfGoalId(self.__prio_FM_area_triangles["STORE_TRIANGLE_DROITE"])
			self.__prio_FM_area_triangles["STORE_TRIANGLE_DROITE"] = temp
		"""
		# Variables TIBOT
		self.__balle_goal_already_swapped = False

	def getBestGoal(self, filet_locked=False):
		if self.__robot_name == "FLUSSMITTEL":
			best_goal = self.__getBestGoalFlussmittel()
		elif self.__robot_name == "TIBOT":
			best_goal = self.__getBestGoalTibot(filet_locked)
		else:
			self.__logger.info("Robot "+str(self.__robot_name)+" inconnu.")
			best_goal = ([], None, None) #type (path, goal, id_elem_goal)

		return best_goal

	def __getTime(self):
		return self.__data["METADATA"]["getGameClock"]

	#FLUSSMITTEL
	def __getBestGoalFlussmittel(self):
		best_goal = ([], None, None) #type (path, goal, id_elem_goal)

		# Log error
		if len(self.__front_triangle_stack) > MAX_FRONT_TRIANGLE_STACK_STORE:
			self.__logger.error("On a stocké plus de triangles qu'on a de place")

		# On tri d'abord par path car le tri est stable
		goals = sorted(self.__available_goals, key=self.__distByPath)

		if len(self.__front_triangle_stack) > 1:
			goals.sort(key=self.__prioStoreTriangle) # car tri stable
		else:
			goals.sort(key=self.__prioTriangle) # car tri stable

		for goal in goals:
			best_elem_goal = self.__getBestElemGoal(goal)
			if best_elem_goal is not None:
				best_goal = best_elem_goal
				break
		
		if best_goal[1] is not None:
			self.__logger.info("Best goal FLUSSMITTEL : " + best_goal[1].getName())
		else:
			self.__logger.info("Best goal FLUSSMITTEL : On a pas trouvé de goal à faire.")

		return best_goal
	
	def __distByPath(self, goal):
		best_path = self.__getBestElemGoal(goal)
		if best_path is not None:
			return best_path[3]
		else:
			return float("Inf")

	def __prioTriangle(self, goal):
		side_gauche = self.__data["FLUSSMITTEL"]["getPosition"][0] < 1500
		if goal.getType() == "triangle" or goal.getType() == "TORCHE":
			if side_gauche:
				if goal.getId() in self.__triangles_gauche:
					return 1
				else:
					return 2
			else:
				if goal.getId() in self.__triangles_gauche:
					return 2
				else:
					return 1
		elif goal.getType() == "TORCHE":
			if side_gauche:
				if goal.getId() == self.__torche_gauche:
					return 1.5
				else:
					return 2.5
			else:
				if goal.getId() == self.__torche_gauche:
					return 2.5
				else:
					return 1.5
		else:
			return 3

	def __prioStoreTriangle(self, goal):
		if goal.getType() == "STORE_TRIANGLE":
			return 0
		else:
			return self.__prioTriangle(goal)

	def __sort_area(self, area):
		return self.__prio_FM_areas.index(area[0])

	def __getGoalsByPriority(self, goals, area):
		def prio(goal):
			best_path = self.__getBestElemGoal(goal)
			if goal.getId() in self.__prio_FM_area_triangles[area]:
				return self.__prio_FM_area_triangles[area].index(goal.getId())
			else:
				return len(self.__prio_FM_area_triangles[area])
		return sorted(goals, key=prio)

	def __getBestElemGoal(self, goal):
		best_elem_goal = None
		best_length = float("Inf")
		position_last_goal = self.__goalsLib.getPositionLastGoal()

		nb_elem_goal = goal.getLenElemGoal()
		for idd in range(nb_elem_goal):
			path = self.__goalsLib.getOrderTrajectoire(goal, idd, position_last_goal)
			#self.__logger.debug("Calcul de trajectoire pour goalName "+str(goal.getName())+" id_elem "+str(idd)+" path "+str(path))
			if path != []:
				if self.__Collision.isCollisionFromGoalsManager(self.__robot_name, path):
					length = self.__goalsLib.pathLen(path)
					if length < best_length:
						best_length = length
						best_elem_goal = (path, goal, idd, length)
				else:
					self.__logger.error("Le pathfinding nous a indiqué un chemin invalide goal "+str(goal.getName())+" elem_id "+str(idd)+"  path "+str(path))
		return best_elem_goal

	#TIBOT
	def __getBestGoalTibot(self, filet_locked):
		best_goal = ([], None, None) #type (path, goal, id_elem_goal)
		best_length = float("Inf")
		best_goal_filet = ([], None, None)
		best_length_filet = float("Inf")
		position_last_goal = self.__goalsLib.getPositionLastGoal()

		#Pour tirer toutes nos balles sur le même mamouth, même l'autre n'est pas dispo
		if self.__balle_goal_already_swapped == False and self.__data["METADATA"]["getGameClock"] > 50000:
			undo_goal = None
			for goal in self.__available_goals:
				if goal.getType() == "BALLES":
					undo_goal = goal

			already_done_goal = None
			for goal in self.__finished_goals:
				if goal.getType() == "BALLES":
					already_done_goal = goal

			if undo_goal is not None and already_done_goal is not None:
				self.__available_goals.remove(undo_goal)
				self.__finished_goals.append(undo_goal)
				self.__finished_goals.remove(already_done_goal)
				self.__available_goals.append(already_done_goal)
				already_done_goal.resetElemAction()
				self.__balle_goal_already_swapped = True

		#Choisi l'objectif le plus proche
		for goal in self.__available_goals:
			nb_elem_goal = goal.getLenElemGoal()
			for idd in range(nb_elem_goal):
				path = self.__goalsLib.getOrderTrajectoire(goal, idd, position_last_goal)
				self.__logger.debug("Calcul de trajectoire pour goalName "+str(goal.getName())+" id_elem "+str(idd)+" path "+str(path))
				if path != []:
					if self.__Collision.isCollisionFromGoalsManager("TIBOT", path):
						length = self.__goalsLib.pathLen(path)
						if goal.getType() != "FILET":
							if length < best_length:
								best_length = length
								best_goal = (path, goal, idd)
						else:
							if length < best_length_filet:
								best_length_filet = length
								best_goal_filet = (path, goal, idd)
					else:
						self.__logger.error("Le pathfinding nous a indiqué un chemin invalide goal "+str(goal.getName())+" elem_id "+str(idd)+"  path "+str(path))
		#Si on a pas d'action possible mis à part le filet
		if best_goal[1] == None:
			best_goal = best_goal_filet

		#Si on est a plus de x secondes, on ne peut pas lock autre chose que le filet
		if self.__data["METADATA"]["getGameClock"] > 75000:
			best_goal = best_goal_filet


		return best_goal

"""def __getGoalsByNorm(self, goals):
		position_last_goal = self.__goalsLib.getPositionLastGoal()
		def dist(goal):
			return hypot(goal.getPosition()[0] - position_last_goal[0], goal.getPosition()[1] - position_last_goal[1])
		return sorted(goals, key=dist)"""

""" Ancien choix d'objectif
		### Phase 1 : Sécurisation des areas (avec priorité)
		if self.__getTime() <= TIME_BETWEEN_PHASE_FM:
			# On récupère et trie les areas
			self.__state_area = []
			for goal in goals:
				if goal.getType() == "STORE_TRIANGLE":
					can_go = False
					best_elem_goal = self.__getBestElemGoal(goal)
					if best_elem_goal is not None:
						can_go = True
					self.__state_area.append([goal.getName(), goal.getAreaStatus(), can_go])
			self.__state_area.sort(key=self.__sort_area)
			# On cherche la meilleure area
			best_area = None
			for area in self.__state_area:
				if area[1] == "EMPTY" and area[2]:
					best_area = area[0]
					break
			# Si on en a trouvé une, on entre dans la phase 1
			if best_area is not None:
				self.__logger.info("Phase 1")
				self.__logger.info("best area = " + best_area)
				goals = self.__getGoalsByPriority(goals, best_area)
				for goal in goals:
					# Si on est obligé de déposer les triangles
					if len(self.__front_triangle_stack) >= MAX_FRONT_TRIANGLE_STACK:
						if len(self.__front_triangle_stack) > MAX_FRONT_TRIANGLE_STACK:
							self.__logger.error("On a stocké plus de triangles qu'on a de place")
						if goal.getName() != best_area:
							continue
						best_elem_goal = self.__getBestElemGoal(goal)
						best_goal = best_elem_goal
						break
					# Sinon on en stocke un maximum
					else:
						if goal.getType() == "STORE_TRIANGLE":
							continue
						best_elem_goal = self.__getBestElemGoal(goal)
						if best_elem_goal is not None:
							best_goal = best_elem_goal
							break

		### Phase 2 : Max de triangles (du bon côté sans se soucier des areas)
		if self.__getTime() > TIME_BETWEEN_PHASE_FM or best_area is None:
			self.__logger.info("Phase 2")
			# TEMP
			for goal in goals:
				if len(self.__front_triangle_stack) >= MAX_FRONT_TRIANGLE_STACK:
					if len(self.__front_triangle_stack) > MAX_FRONT_TRIANGLE_STACK:
						self.__logger.error("On a stocké plus de triangle qu'on a de place")
					if goal.getType() != "STORE_TRIANGLE":
						continue
				else:
					if goal.getType() == "STORE_TRIANGLE":
						continue
				best_elem_goal = self.__getBestElemGoal(goal)
				if best_elem_goal is not None:
					best_goal = best_elem_goal
					break

		"""
