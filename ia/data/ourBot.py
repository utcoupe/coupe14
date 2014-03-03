# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""


class OurBot():
	def __init__(self, constantes, communication, arduinoConstantes, addressOther, addressAsserv, largeur, longueur):
		#Constantes
		self.communication = communication
		self.addressOther = addressOther
		self.addressAsserv = addressAsserv

		self.largeur = largeur 
		self.longueur = longueur


		#Valeurs récupérées (read-only)
		self.positionX = 0
		self.positionY = 0
		self.angle = 0.0

		#Variables
		self.orders = None

	#Getter
	def getPositon(self):
		return (self.positionX, self.positionY)

	#utilise les données en provenance de nos robots pour mettre à jour les données de la classe
	def majPosition(self, arguments):
		self.positionX = arguments[0]
		self.positionY = arguments[1]
		self.angle = arguments[2]