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

		# state zone
		self.__TIME_PHASE = {"1": 50000, "2": 75000, "3": 90000}

		# Priorité
		self.__prio_FM_zones = ["ZONE_GAUCHE", "ZONE_DROITE", "ZONE_CENTRALE"]
		self.__prio_FM_zone_triangles = {"ZONE_CENTRALE": [17,7,6,5,4,18,1], "ZONE_GAUCHE": [8,17,9,7,5], "ZONE_DROITE": [7,5,4,18,3]}
		if self.__our_color == "YELLOW":
			self.__prio_FM_zones = ["ZONE_DROITE", "ZONE_GAUCHE", "ZONE_CENTRALE"]
			self.__prio_FM_zone_triangles["ZONE_CENTRALE"] = self.__goalsLib.reverseTabOfGoalId(self.__prio_FM_zone_triangles["ZONE_CENTRALE"])
			self.__prio_FM_zone_triangles["ZONE_GAUCHE"] = self.__goalsLib.reverseTabOfGoalId(self.__prio_FM_zone_triangles["ZONE_GAUCHE"])
			self.__prio_FM_zone_triangles["ZONE_DROITE"] = self.__goalsLib.reverseTabOfGoalId(self.__prio_FM_zone_triangles["ZONE_DROITE"])

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

		# On tri d'abord par path car le tri est stable
		goals = sorted(self.__available_goals, key=self.__distByPath)
		"""
		### Phase 1 : Sécurisation des zones (avec priorité)
		best_zone = None
		if self.__getTime() <= self.__TIME_PHASE["1"]:
			for zone in self.__prio_FM_zones:
				if self.__state_zone[zone] == self.__ZONE_LIBRE:
					best_zone = zone
					break
			if best_zone is not None:
				goals = self.__getGoalsByPriority(goals, zone)
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
		### Phase 2 : Max de triangles (du bon côté sans se soucier des zones)
		if (self.__getTime() > self.__TIME_PHASE["1"] and self.__getTime() <= self.__TIME_PHASE["2"]) or (self.__getTime() <= self.__TIME_PHASE["1"] and best_zone is None):
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
		### Phase 3 : Zero triangle inside !
		elif True or self.__getTime() <= self.__TIME_PHASE["3"]:
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
		for goal in goals:
			if len(self.__front_triangle_stack) >= MAX_FRONT_TRIANGLE_STACK_STORE:
				if len(self.__front_triangle_stack) > MAX_FRONT_TRIANGLE_STACK_STORE:
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
		
		return best_goal

	
	def __distByPath(self, goal):
		best_path = self.__getBestElemGoal(goal)
		if best_path is not None:
			return best_path[3]
		else:
			return float("Inf")
	"""
	def __getGoalsByPriority(self, goals, zone):
		def prio(goal):
			best_path = self.__getBestElemGoal(goal)
			if goal.getId() in self.__prio_FM_zone_triangles[zone]:
				return self.__prio_FM_zone_triangles[zone].index(goal.getId())
			else:
				return len(self.__prio_FM_zone_triangles[zone])
		return sorted(goals, key=prio)"""

	def __getBestElemGoal(self, goal):
		best_elem_goal = None
		best_length = float("Inf")
		position_last_goal = self.__goalsLib.getPositionLastGoal()

		nb_elem_goal = goal.getLenElemGoal()
		for idd in range(nb_elem_goal):
			path = self.__goalsLib.getOrderTrajectoire(goal, idd, position_last_goal)
			#self.__logger.debug("Calcul de trajectoire pour goalName "+str(goal.getName())+" id_elem "+str(idd)+" path "+str(path))
			if path != []:
				if self.__data["METADATA"]["getGameClock"] < BEGIN_CHECK_COLLISION or self.__Collision.isCollisionFromGoalsManager(self.__robot_name, path):
					length = self.__goalsLib.pathLen(path)
					if length < best_length:
						best_length = length
						best_elem_goal = (path, goal, idd, length)
				else:
					self.__logger.warning("Le pathfinding nous a indiqué un chemin invalide goal "+str(goal.getName())+" elem_id "+str(idd)+"  path "+str(path))
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
					if self.__data["METADATA"]["getGameClock"] < BEGIN_CHECK_COLLISION or self.__Collision.isCollisionFromGoalsManager("TIBOT", path):
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
