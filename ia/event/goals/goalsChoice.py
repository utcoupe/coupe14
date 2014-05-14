# -*- coding: utf-8 -*-
"""
Class used to choose what to do
"""

import logging
from math import *

from .goal import *
from .ElemGoal import *
from .navigation import *
from .goalsLibrary import *

class GoalsChoice:
	def __init__(self, robot_name, data, goalsLib, our_color):
		self.__robot_name = robot_name
		self.__data = data
		self.__goalsLib = goalsLib
		self.__our_color = our_color
		self.__logger = logging.getLogger(__name__)

	def getBestGoal(self, goals):
		best_goal = ([], None, None) #type (path, goal, id_elem_goal)
		best_length = float("Inf")

		if self.__robot_name == "FLUSSMITTEL":
			for goal in goals:
				nb_elem_goal = goal.getLenElemGoal()
				for idd in range(nb_elem_goal):
					path = self.__goalsLib.getOrderTrajectoire(goal, idd)
					if path != []:
						length = self.__goalsLib.pathLen(path)
						if length < best_length:
							best_length = length
							best_goal = (path, goal, idd)
		elif self.__robot_name == "TIBOT":
			for goal in goals:
				nb_elem_goal = goal.getLenElemGoal()
				for idd in range(nb_elem_goal):
					path = self.__goalsLib.getOrderTrajectoire(goal, idd)
					if path != []:
						length = self.__goalsLib.pathLen(path)
						if length < best_length:
							best_length = length
							best_goal = (path, goal, idd)
		else:
			self.__logger.info("Robot "+str(self.__robot_name)+" inconnu.")
		return best_goal
