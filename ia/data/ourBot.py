# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""

from . import pullData

class OurBot():
	def __init__(self, communication, largeur, longueur):
		#Constantes
		self.communication = communication
		self.pullData = pullData.PullData(communication)
		self.largeur = largeur #en mm
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