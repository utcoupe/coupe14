# -*- coding: utf-8 -*-
"""
Classe pour nos robots et pour les robots adverses
"""

class ourBot():
	def __init__(self):
		#Constantes
		self.largeur = 10 #en mm
		self.longueur = 10 

		#Valeurs récupérées (read-only)
		self.positionX = 0
		self.positionY = 0
		self.angle = 0

		#Variables
		self.orders = None

	#Getter
	def getPositon(self):
		return (self.positionX, self.positionY)

class enemyBot():
	def __init__(self):
		#Constants
		self.largeur = 10 
		self.longueur = 10

		#Valeurs récupérées (read-only)
		self.positionX = 0
		self.positionY = 0