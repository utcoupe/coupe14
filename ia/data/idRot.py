# -*- coding: utf-8 -*-
"""
Gere des id rotationnelle de 0 à 255, on les utilisent pour les id d'actions
"""

class IdRot:
	def __init__(self):
		self.__max = 29999 #ne peut être modifié indépendament du eventManager
		self.__id = self.__max

	def getId(self):
		return self.__id

	def idIncrementation(self):
		self.__id += 1
		if self.__id > self.__max:
			self.__id = 0

		return self.__id

	#ne devrait être utilisé qu'en cas d'annulation d'objectif
	def idReduce(self, value):
		self.__id -= value
		if self.__id < 0:
			self.__id += self.__max + 1

		return self.__id


