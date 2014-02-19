# -*- coding: utf-8 -*-
"""
Classe pour les robots adverses
"""

from . import pullData

class enemyBot():
	def __init__(self):
		#Constants
		self.largeur = 10 
		self.longueur = 10

		#Valeurs récupérées (read-only)
		self.positionX = 0
		self.positionY = 0