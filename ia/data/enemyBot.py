# -*- coding: utf-8 -*-
"""
Classe pour les robots adverses
"""



class EnemyBot():
	def __init__(self, constantes, largeur, longueur, rayon):
		#Constants
		self.largeur = largeur
		self.longueur = longueur
		self.rayon = rayon

		#Valeurs récupérées (read-only)
		self.positionX = 0
		self.positionY = 0

	def getPositon(self):
		return (self.positionX, self.positionY)