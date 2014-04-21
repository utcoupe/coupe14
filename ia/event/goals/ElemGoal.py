# -*- coding: utf-8 -*-
"""
Class used to reprsent an elemetary goal, which is on entry of an objectif
"""


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
		self.__elem_action = elem_action
		self.__already_step_over = False

	def getFirstElemAction(self):
		if self.__elem_action:
			action_list = []
			continu = True
			for action in self.__elem_action:
				if continu:
					action_list.append(action)
				if action == "END" or action == "STEP_OVER":
					continu = False
					break
			return action_list
		else:
			return []

	def removeFirstElemAction(self):
		if self.__already_step_over:
			if self.__elem_action:
				action = self.__elem_action.popleft()
				while action != "END" and action != "STEP_OVER":
					action = self.__elem_action.popleft()
		else:
			self.__already_step_over = True

	def getPositionAndAngle(self):
		return (self.__x, self.__y, self.__angle)