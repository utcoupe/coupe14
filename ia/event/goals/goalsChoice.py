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
	def __init__(self, robot_name, data, goalsLib):
		self.__robot_name = robot_name
		self.__data = data
		self.__goalsLib = goalsLib
		self.__logger = logging.getLogger(__name__)

	def getBestGoal(self, goals):
		best_goal = ([], None, None) #type (path, id_goal, id_elem_goal)
		best_length = float("Inf")

		for goal in goals:
			nb_elem_goal = goal.getLenElemGoal()
			for idd in range(nb_elem_goal):
				path = self.__goalsLib.getOrderTrajectoire(goal, idd)
				if path != []:
					length = self.__goalsLib.pathLen(path)
					if length < best_length:
						best_length = length
						best_goal = (path, goal, idd)
		return best_goal