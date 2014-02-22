# -*- coding: utf-8 -*-
"""
Classe globale pour toutes les données, on y instancie les objets
"""


from . import ourBot
from . import enemyBot
from . import tourelle
from . import other

class Data():
	def __init__(self, communication, constantes, arduinoConstantes):

		self.flussmittel = ourBot.OurBot(constantes, communication, arduinoConstantes, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV', constantes.largeurFM, constantes.longueurFM)
		self.tibot = ourBot.OurBot(constantes, communication, arduinoConstantes, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV', constantes.largeurTB, constantes.longueurTB)

		if constantes.numberOfenemy >= 1:
			self.smallEnemyBot = enemyBot.EnemyBot(constantes, constantes.largeurBigEnemy, constantes.longueurBigEnemy)
		if constantes.numberOfenemy >= 2:
			self.bigEnemyBot = enemyBot.EnemyBot(constantes, constantes.largeurSmallEnemy, constantes.longueurSmallEnemy)

		self.tourelle = tourelle.Tourelle(constantes, communication, arduinoConstantes, 'ADDR_HOKUYO')
		self.other = other.Other(constantes)
