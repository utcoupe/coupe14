# -*- coding: utf-8 -*-
"""
Classe pour les robots adverses
"""

from constantes import *
from math import sqrt

class EnemyBot():
	def __init__(self, rayon):
		#Constants
		self.__rayon = rayon


		#Valeurs récupérées (read-only)
		self.__positionX = 0
		self.__positionY = 0

	def getPosition(self):
		return (self.__positionX, self.__positionY)
	def getRayon(self):
		return self.__rayon
