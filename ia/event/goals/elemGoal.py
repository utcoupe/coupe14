# -*- coding: utf-8 -*-
"""
Class used to reprsent an elemetary goal, which is on entry of an objectif
"""

import copy

class ElemGoal:
	def __init__(self, id, x, y, angle, points, priority, duration, color, script_only, elem_action):
		self.__id 		= id
		self.__x 		= x
		self.__y 		= y
		self.__angle 	= angle
		self.__points 	= points
		self.__priority	= priority
		self.__duration	= duration
		self.__color	= color
		self.__script_only = script_only
		self.__elem_action_base = copy.deepcopy(elem_action)
		self.__elem_action_temp = copy.deepcopy(elem_action)
		self.__already_step_over = False
		self.__coord_bras = None
		self.__coord_bras_verified = False

	def getCoordBras(self):
		return self.__coord_bras

	def getCoordBrasVerified(self):
		return self.__coord_bras_verified

	def getScriptOnly(self):
		return self.__script_only

	def getNextElemAction(self):
		return self.__elem_action_temp

	def getPositionAndAngle(self):
		return (self.__x, self.__y, self.__angle)

	def getColor(self):
		return self.__color

	def getPoints(self):
		return self.__points

	def switchColor(self):
		if self.__color == "RED":
			self.__color = "YELLOW"
		else:
			self.__color = "RED"

	def reset_elem_action(self):
		self.__elem_action_temp = copy.deepcopy(self.__elem_action_base)

	def setCoordBras(self, x, y):
		self.__coord_bras = (x,y)

	def setCoordBrasVerified(self, verified):
		self.__coord_bras_verified = verified
