# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""

from . import pullData

class OurBot():
	def __init__(self, constantes, communication, arduinoConstantes, addressOther, addressAsserv, largeur, longueur):
		#Constantes
		self.communication = communication
		self.addressOther = addressOther
		self.addressAsserv = addressAsserv

		self.pullDataOther = pullData.PullData(constantes, communication, arduinoConstantes['address'][self.addressOther])
		self.pullDataAsserv = pullData.PullData(constantes, communication, arduinoConstantes['address'][self.addressAsserv])
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