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
	def __init__(self, robot_name, data, goalsLib, Collision, our_color, back_triangle_stack, front_triangle_stack, balles_lancees):
		self.__logger = logging.getLogger(__name__)

		self.__robot_name = robot_name
		self.__data = data
		self.__goalsLib = goalsLib
		self.__Collision = Collision
		self.__our_color = our_color

		# Variables FLUSSMITTEL
		self.__back_triangle_stack = back_triangle_stack
		self.__front_triangle_stack = front_triangle_stack
		"""
		self.__ZONE_DEPOT_CENTRALE_VIDE = 0
		self.__ZONE_DEPOT_GAUCHE_VIDE = 0
		self.__ZONE_DEPOT_DROITE_VIDE = 0
		"""

		# Priorité
		if self.__our_color == "RED":
			self.__prio_tibot_goals = ["Fresque", "BALLES GAUCHE", "BALLES DROITE", "TIR_FILET"] # goal.name
			self.__prio_tibot_balles = {"BALLES GAUCHE": 4, "BALLES DROITE": 2} # elem_goal.points
		else: # Yellow, idem qu'au dessus pour les variables
			self.__prio_tibot_goals = ["Fresque", "BALLES DROITE", "BALLES GAUCHE", "TIR_FILET"]
			self.__prio_tibot_balles = {"BALLES GAUCHE": 2, "BALLES DROITE": 4}

		# Variables TIBOT
		self.__balles_lancees = balles_lancees

	def getBestGoal(self, goals, filet_locked=False):
		if self.__robot_name == "FLUSSMITTEL":
			best_goal = self.__getBestGoalFlussmittel(goals)
		elif self.__robot_name == "TIBOT":
			best_goal = self.__getBestGoalTibot(goals, filet_locked)
		else:
			self.__logger.info("Robot "+str(self.__robot_name)+" inconnu.")
			best_goal = ([], None, None) #type (path, goal, id_elem_goal)

		return best_goal

	#FLUSSMITTEL

	def __getBestGoalFlussmittel(self, goals):
		best_goal = ([], None, None) #type (path, goal, id_elem_goal)
		best_length = float("Inf")
		position_last_goal = self.__goalsLib.getPositionLastGoal()
		
		for goal in goals:
			if len(self.__front_triangle_stack) >= MAX_FRONT_TRIANGLE_STACK:
				if len(self.__front_triangle_stack) > MAX_FRONT_TRIANGLE_STACK:
					self.__logger.error("On a stocké plus de triangle qu'on a de place")

				if goal.getType() != "STORE_TRIANGLE":
					continue
			else:
				if goal.getType() == "STORE_TRIANGLE":
					continue
			nb_elem_goal = goal.getLenElemGoal()
			for idd in range(nb_elem_goal):
				path = self.__goalsLib.getOrderTrajectoire(goal, idd, position_last_goal)
				if path != []:
					if self.__Collision.isCollisionFromGoalsManager("FLUSSMITTEL", path):
						length = self.__goalsLib.pathLen(path)
						if length < best_length:
							best_length = length
							best_goal = (path, goal, idd)
					else:
						self.__logger.error("Le pathfinding nous a indiqué un chemin invalide goal "+str(goal.getName())+" elem_id "+str(idd)+"  path "+str(path))

		return best_goal

	#TIBOT
	def __getBestGoalTibot(self, goals, filet_locked):
		best_goal = ([], None, None) #type (path, goal, id_elem_goal)
		best_length = float("Inf")
		best_goal_filet = ([], None, None)
		best_length_filet = float("Inf")
		position_last_goal = self.__goalsLib.getPositionLastGoal()

		for goal in goals:
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

		#Si on est à plus de 80s de jeu, on force le choix du filet
		if (best_goal[1] == None or self.__data["METADATA"]["getGameClock"] > 80000) and best_goal_filet[1] != None:
			best_goal = best_goal_filet

		#Si on a le temps de refaire un objectif avant le filet, on le fait
		if filet_locked == True and self.__data["METADATA"]["getGameClock"] > 60000:
			return ([], None, None)

		return best_goal
