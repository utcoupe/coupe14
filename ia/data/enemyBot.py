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
		self.__positionX = 2500#TODO, parametrage en focntion du coté où on commence
		self.__positionY = 1500

	def getPosition(self):
		return (self.__positionX, self.__positionY)

	def getRayon(self):
		return self.__rayon

	def setPosition(self, position):
		self.__positionX = position.x
		self.__positionY = position.y
