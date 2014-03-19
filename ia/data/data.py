# -*- coding: utf-8 -*-
"""
Classe globale pour toutes les données, on y instancie les objets
"""
from constantes import *

from .ourBot import *
from .enemyBot import *
from .tourelle import *
from .metaData import *
from .pullData import *

class Data():
	def __init__(self, Communication, arduino_constantes):
		self.Flussmittel = None
		self.Tibot = None
		self.SmallEnemyBot = None
		self.BigEnemyBot = None
		self.Tourelle = None
		self.MetaData = MetaData()


		#Instantation des objets
		if ENABLE_FLUSSMITTEL == True:
			self.Flussmittel = OurBot('FLUSSMITTEL', Communication, arduino_constantes, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV', LARGEUR_FLUSSMITTEL, LONGUEUR_FLUSSMITTEL)
			self.Flussmittel.loadActionScript("data/flussmittel.xml")

		if ENABLE_TIBOT == True:
			self.Tibot = OurBot('TIBOT', Communication, arduino_constantes, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV', LARGEUR_TIBOT, LONGUEUR_TIBOT)
			self.Tibot.loadActionScript("data/tibot.xml")

		if NUMBER_OF_ENEMY >= 1:
			self.SmallEnemyBot = EnemyBot(RAYON_BIG_ENEMY)
		if NUMBER_OF_ENEMY >= 2:
			self.BigEnemyBot = EnemyBot(RAYON_SMALL_ENEMY)

		if ENABLE_TOURELLE == True:
			self.Tourelle = Tourelle(Communication, arduino_constantes, 'ADDR_HOKUYO')

		self.PullData = PullData(Communication, (self.Flussmittel, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV'), (self.Tibot, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV'), self.SmallEnemyBot, self.BigEnemyBot, (self.Tourelle, arduino_constantes['address']['ADDR_HOKUYO']), PULL_PERIODE)

		
