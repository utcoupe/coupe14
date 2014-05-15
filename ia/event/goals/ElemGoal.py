# -*- coding: utf-8 -*-
"""
Class used to reprsent an elemetary goal, which is on entry of an objectif
"""

import copy

class ElemGoal:
	def __init__(self, id, x, y, angle, points, priority, duration, color, elem_action):
		self.__id 		= id
		self.__x 		= x
		self.__y 		= y
		self.__angle 	= angle
		self.__points 	= points
		self.__priority	= priority
		self.__duration	= duration
		self.__color	= color
		self.__elem_action_base = copy.deepcopy(elem_action)
		self.__elem_action_temp = copy.deepcopy(elem_action)
		self.__already_step_over = False

	def getFirstElemAction(self):
		if self.__elem_action_temp:
			action_list = []
			continu = True
			for action in self.__elem_action_temp:
				if continu:
					action_list.append(action)
				if action[0] == "END" or action[0] == "STEP_OVER":
					continu = False
					break
			return action_list
		else:
			return []

	def removeFirstElemAction(self):
		if self.__elem_action_temp:
			action = self.__elem_action_temp.popleft()
			while action[0] != "END" and action[0] != "STEP_OVER":
				action = self.__elem_action_temp.popleft()

	def resetElemAction(self):
		self.__elem_action_temp = copy.deepcopy(self.__elem_action_base)

	def getPositionAndAngle(self):
		return (self.__x, self.__y, self.__angle)

	def getColor(self):
		return self.__color

	def switchColor(self):
		if self.__color == "RED":
			self.__color = "YELLOW"
		else:
			self.__color = "RED"