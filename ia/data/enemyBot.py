# -*- coding: utf-8 -*-
"""
Classe pour les robots adverses
"""



class EnemyBot():
	def __init__(self, constantes, largeur, longueur):
		#Constants
		self.largeur = largeur
		self.longueur = longueur

		#Valeurs récupérées (read-only)
		self.positionX = 0
		self.positionY = 0