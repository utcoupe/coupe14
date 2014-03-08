# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""

from constantes import *
from math import sqrt
import logging

class OurBot():
	def __init__(self, communication, arduino_constantes, addressOther, addressAsserv, largeur, longueur):
		#Constantes
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__communication = communication
		self.__addressOther = addressOther
		self.__addressAsserv = addressAsserv

		self.__largeur = largeur 
		self.__longueur = longueur
		self.__rayon = sqrt(largeur**2 + longueur**2)


		#Valeurs récupérées (read-only)
		self.__positionX = 0
		self.__positionY = 0
		self.__angle = 0.0

		#Variables
		self.__orders = None

	#Getter
	def getPositon(self):
		return (self.__positionX, self.__positionY)
	def getRayon(self):
		return self.__rayon

	#setter

	#utilise les données en provenance de nos robots pour mettre à jour les données de la classe
	def majPosition(self, arguments):
		self.__positionX = arguments[0]
		self.__positionY = arguments[1]
		self.__angle = arguments[2]
