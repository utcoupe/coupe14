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
		self.MetaData = metaData.MetaData(Constantes)


		#Instantation des objets
		if self.Constantes.enable_flussmittel == True:
			self.Flussmittel = ourBot.OurBot(Constantes, Communication, arduino_constantes, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV', Constantes.largeur_flussmittel, Constantes.longueur_flussmittel)

		if self.Constantes.enable_tibot == True:
			self.Tibot = ourBot.OurBot(Constantes, Communication, arduino_constantes, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV', Constantes.largeur_tibot, Constantes.longueur_tibot)

		if self.Constantes.number_of_enemy >= 1:
			self.SmallEnemyBot = enemyBot.EnemyBot(Constantes, Constantes.largeurBigEnemy, Constantes.longueurBigEnemy)
		if Constantes.number_of_enemy >= 2:
			self.BigEnemyBot = enemyBot.EnemyBot(Constantes, Constantes.largeurSmallEnemy, Constantes.longueurSmallEnemy)

		if self.Constantes.enable_tourelle == True:
			self.Tourelle = tourelle.Tourelle(Constantes, Communication, arduino_constantes, 'ADDR_HOKUYO')

		self.PullData = pullData.PullData(Communication, (self.Flussmittel, arduino_constantes['address']['ADDR_FLUSSMITTEL_OTHER'], arduino_constantes['address']['ADDR_FLUSSMITTEL_ASSERV']), (self.Tibot, arduino_constantes['address']['ADDR_TIBOT_OTHER'], arduino_constantes['address']['ADDR_TIBOT_ASSERV']), self.SmallEnemyBot, self.BigEnemyBot, (self.Tourelle, arduino_constantes['address']['ADDR_HOKUYO']), Constantes.pull_periode)

		
