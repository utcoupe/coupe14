# -*- coding: utf-8 -*-
"""
Classe globale pour toutes les données, on y instancie les objets
"""


from . import ourBot
from . import enemyBot
from . import tourelle
from . import other

class Data():
	def __init__(self, communication, constantes):

		self.flussmittel = ourBot.OurBot(communication, constantes.largeurFM, constantes.longueurFM)
		self.tibot = ourBot.OurBot(communication, constantes.largeurTB, constantes.longueurTB)

		if constantes.numberOfenemy >= 1:
			self.smallEnemyBot = enemyBot.EnemyBot(constantes.largeurBigEnemy, constantes.longueurBigEnemy)
		if constantes.numberOfenemy >= 2:
			self.bigEnemyBot = enemyBot.EnemyBot(constantes.largeurSmallEnemy, constantes.longueurSmallEnemy)

		self.tourelle = tourelle.Tourelle(communication)
		self.other = other.Other(constantes.numberOfenemy)
