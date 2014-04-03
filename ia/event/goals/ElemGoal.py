# -*- coding: utf-8 -*-
"""
Class used to reprsent an elemetary goal, which is on entry of an objectif
"""


class ElemGoal:
	def __init__(self, id, x, y, angle, points, priority, duration, color, id_script):
		self.__id 		= id
		self.__x 		= x
		self.__y 		= y
		self.__angle 	= angle
		self.__points 	= points
		self.__priority	= priority
		self.__duration	= duration
		self.__color	= color
		self.__id_script = id_script

	def getIdScript(self):
		return self.__id_script

	def getPosition(self):
		return (self.__x, self.__y, self.__angle)