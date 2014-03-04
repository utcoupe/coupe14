# -*- coding: utf-8 -*-
"""
Classe globale pour toutes les données, on y instancie les objets
"""

from . import ourBot
from . import enemyBot
from . import tourelle
from . import metaData
from . import pullData

class Data():
	def __init__(self, Communication, Constantes, arduino_constantes):
		self.Constantes = Constantes

		self.Flussmittel = None
		self.Tibot = None
		self.SmallEnemyBot = None
		self.BigEnemyBot = None
		self.Tourelle = None
		self.MetaData = metaData.MetaData(Constantes)


		#Instantation des objets
		if self.Constantes.ENABLE_FLUSSMITTEL == True:
			self.Flussmittel = ourBot.OurBot(Constantes, Communication, arduino_constantes, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV', Constantes.LARGEUR_FLUSSMITTEL, Constantes.LONGUEUR_FLUSSMITTEL)

		if self.Constantes.ENABLE_TIBOT == True:
			self.Tibot = ourBot.OurBot(Constantes, Communication, arduino_constantes, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV', Constantes.LARGEUR_TIBOT, Constantes.LONGUEUR_TIBOT)

		if self.Constantes.NUMBER_OF_ENEMY >= 1:
			self.SmallEnemyBot = enemyBot.EnemyBot(Constantes, Constantes.LARGEUR_BIG_ENEMY, Constantes.LONGUEUR_BIG_ENEMY)
		if Constantes.NUMBER_OF_ENEMY >= 2:
			self.BigEnemyBot = enemyBot.EnemyBot(Constantes, Constantes.LARGEUR_SMALL_ENEMY, Constantes.LONGUEUR_SMALL_ENEMY)

		if self.Constantes.ENABLE_TOURELLE == True:
			self.Tourelle = tourelle.Tourelle(Constantes, Communication, arduino_constantes, 'ADDR_HOKUYO')

		self.PullData = pullData.PullData(Communication, (self.Flussmittel, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV'), (self.Tibot, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV'), self.SmallEnemyBot, self.BigEnemyBot, (self.Tourelle, arduino_constantes['address']['ADDR_HOKUYO']), Constantes.PULL_PERIODE)

		
