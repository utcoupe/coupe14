# -*- coding: utf-8 -*-
"""
Classe globale pour toutes les données, on y instancie les objets
"""


from . import ourBot
from . import enemyBot
from . import tourelle
from . import other

class data():
	def __init__(self, communication, constantes):

		self.FM = ourBot.ourBot(communication, constantes.largeurFM, constantes.longueurFM)
		self.tiBot = ourBot.ourBot(communication, constantes.largeurTB, constantes.longueurTB)

		if constantes.numberOfenemy >= 1:
			self.smallEnemyBot = enemyBot.enemyBot(constantes.largeurBigEnemy, constantes.longueurBigEnemy)
		if constantes.numberOfenemy >= 2:
			self.bigEnemyBot = enemyBot.enemyBot(constantes.largeurSmallEnemy, constantes.longueurSmallEnemy)

		self.tourelle = tourelle.tourelle(communication)
		self.other = other.other(constantes.numberOfenemy)
