# -*- coding: utf-8 -*-
"""
Gere des id rotationnelle de 0 à 255, on les utilisent pour les id d'actions
"""

class IdRot:
	def __init__(self):
		self.__min = 0
		self.__max = 29999
		self.__id = 29999

	def getId(self):
		return self.__id

	def idIncremntation(self):
		self.__id += 1
		if self.__id > self.__max:
			self.__id = self.__min

		return self.__id

	def setId(self, value):
		self.__id = value


