# -*- coding: utf-8 -*-
"""
Class used to reprsent an elemetary goal, which is on entry of an objectif
"""


class ElemGoal:
	def __init__(self, x, y, angle, points, priority, duration, id_script):
		self.__x 		= x
		self.__y 		= y
		self.__angle 	= angle
		self.__points 	= points
		self.__priority	= priority
		self.__duration	= duration
		self.__id_script = id_script