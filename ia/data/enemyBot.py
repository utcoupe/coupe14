# -*- coding: utf-8 -*-
"""
Classe pour les robots adverses
"""

from constantes import *
from math import sqrt

class EnemyBot():
	def __init__(self, rayon, ia_color, name):
		#Constants
		self.__rayon = rayon
		self.__ia_color = ia_color
		self.__name = name #type "SMALL" ou "BIG"

		#Valeurs récupérées (read-only)
		
		if name == "BIG":
			if ia_color == "YELLOW":
				self.__positionX = FIRST_POSITION_BIG_RED_ENNEMY[0]
				self.__positionY = FIRST_POSITION_BIG_RED_ENNEMY[1]
			else:
				self.__positionX = 3000-FIRST_POSITION_BIG_RED_ENNEMY[0]
				self.__positionY = FIRST_POSITION_BIG_RED_ENNEMY[1]
		else:
			if ia_color == "YELLOW":
				self.__positionX = FIRST_POSITION_SMALL_RED_ENNEMY[0]
				self.__positionY = FIRST_POSITION_SMALL_RED_ENNEMY[1]
			else:
				self.__positionX = 3000 - FIRST_POSITION_SMALL_RED_ENNEMY[0]
				self.__positionY = FIRST_POSITION_SMALL_RED_ENNEMY[1]



	def getPosition(self):
		return (self.__positionX, self.__positionY)

	def getRayon(self):
		return self.__rayon

	def setPosition(self, position):
		self.__positionX = position.x
		self.__positionY = position.y
