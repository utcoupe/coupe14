# -*- coding: utf-8 -*-
"""
Functions used in goalsManager and goalsChoice
"""

import logging
from math import *

from collections import deque
from .goal import *
from .elemGoal import *
from .navigation import *

class GoalsLibrary:
	def __init__(self, robot_name, data, blocked_goals, pathfinding):
		self.__robot_name = robot_name
		self.__data = data
		self.__logger = logging.getLogger(__name__)
		self.__blocked_goals = blocked_goals
		self.__PathFinding = pathfinding

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

		self.__reverse_table[(6,0)] = (5,0)
		self.__reverse_table[(5,0)] = (6,0)

		self.__reverse_table[(10,0)] = (10,1)

		self.__reverse_table[(11,0)] = (12,0)
		self.__reverse_table[(11,1)] = (12,1)
		self.__reverse_table[(12,0)] = (11,0)
		self.__reverse_table[(12,1)] = (11,1)

		self.__reverse_table[(13,0)] = (13,1)
		self.__reverse_table[(13,1)] = (13,0)

		self.__reverse_table[(17,0)] = (17,0)
		self.__reverse_table[(17,1)] = (17,1)
		self.__reverse_table[(17,2)] = (17,2)
		self.__reverse_table[(17,3)] = (17,3)

		self.__reverse_table[(18,0)] = (18,0)
		self.__reverse_table[(18,1)] = (18,1)
		self.__reverse_table[(18,2)] = (18,2)
		self.__reverse_table[(18,3)] = (18,3)


	def reverseGoalId(self, goal_id, elem_id = 0):
		return self.__reverse_table[(goal_id, elem_id)]

	def reverseTabOfGoalId(self, tab):
		ret = []
		for idd in tab:
			ret.append(self.__reverse_table[(idd, 0)][0])

		return ret

	def getPositionLastGoal(self, position_depart_speciale=None):
		if position_depart_speciale is not None:
			position_last_goal = position_depart_speciale
			#self.__logger.debug("Position from position_depart_speciale" + str(position_last_goal))
		elif self.__blocked_goals:
			last_goal = self.__blocked_goals[-1]
			position_last_goal = last_goal.getElemGoalLocked().getPositionAndAngle()
			#self.__logger.debug("Position from queue" + str(position_last_goal))
		else:
			position_last_goal = self.__data[self.__robot_name]["getPositionAndAngle"]
			#self.__logger.debug("Position from data" + str(position_last_goal))

		return position_last_goal

	def getOrderTrajectoire(self, goal, elem_goal_id, position_last_goal):
		"""Il faut mettre à jour les polygones avant d'utiliser cette fonction"""
		position_to_reach = goal.getElemGoalOfId(elem_goal_id).getPositionAndAngle()
		path = self.__PathFinding.getPath((position_last_goal[0], position_last_goal[1]), (position_to_reach[0], position_to_reach[1]), enable_smooth=True)

		return path

	def tupleTrajectoireToDeque(self, tuple_trajectoire_list):
		order_list = deque()
		for tuple in tuple_trajectoire_list:
			order_list.append(('A_GOTO', [tuple[0], tuple[1]]))
		return order_list

	def pathLen(self, path):
		length = 0.0
		begin_point = (0,0)
		if path:
			begin_point = path[0]

		for point in path:
			length += hypot(int(point[0]) - int(begin_point[0]), int(point[1]) - int(begin_point[1]))
			begin_point = point

		return length