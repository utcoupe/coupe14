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
	def __init__(self, Communication, arduino_constantes, ia_color):
		self.Flussmittel = None
		self.Tibot = None
		self.SmallEnemyBot = None
		self.BigEnemyBot = None
		self.Tourelle = None
		self.ComputeHokuyoData = None
		self.MetaData = MetaData()


		#Instantation des objets
		if ENABLE_FLUSSMITTEL == True:
			self.Flussmittel = OurBot('FLUSSMITTEL', Communication, arduino_constantes, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV', LARGEUR_FLUSSMITTEL, LONGUEUR_FLUSSMITTEL)

		if ENABLE_TIBOT == True:
			self.Tibot = OurBot('TIBOT', Communication, arduino_constantes, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV', LARGEUR_TIBOT, LONGUEUR_TIBOT)

		if NUMBER_OF_ENEMY >= 1:
			self.SmallEnemyBot = EnemyBot(RAYON_SMALL_ENEMY, ia_color, "SMALL")
		if NUMBER_OF_ENEMY >= 2:
			self.BigEnemyBot = EnemyBot(RAYON_BIG_ENEMY, ia_color, "BIG")

		if ENABLE_TOURELLE == True:
			self.Tourelle = Tourelle(self.Flussmittel, self.Tibot, self.BigEnemyBot, self.SmallEnemyBot, self.MetaData,  Communication, arduino_constantes, 'ADDR_TOURELLE')

		self.__PullData = PullData(Communication, arduino_constantes, (self.Flussmittel, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV'), (self.Tibot, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV'), self.SmallEnemyBot, self.BigEnemyBot, self.ComputeHokuyoData, (self.Tourelle, 'ADDR_TOURELLE'), self.MetaData)

	def startPullData(self):
		self.__PullData.start()

	def dataToDico(self):
		data = {}

		if self.Flussmittel is not None:
			system = self.Flussmittel
			data["FLUSSMITTEL"] = {}
			data["FLUSSMITTEL"]["getPosition"] = system.getPosition()
			data["FLUSSMITTEL"]["getPositionAndAngle"] = system.getPositionAndAngle()
			data["FLUSSMITTEL"]["getRayon"] = system.getRayon()
		else:
			data["FLUSSMITTEL"] = None

		if self.Tibot is not None:
			system = self.Tibot
			data["TIBOT"] = {}
			data["TIBOT"]["getPosition"] = system.getPosition()
			data["TIBOT"]["getPositionAndAngle"] = system.getPositionAndAngle()
			data["TIBOT"]["getRayon"] = system.getRayon()
		else:
			data["TIBOT"] = None

		if self.Tourelle is not None:
			system = self.Tourelle
			data["TOURELLE"] = {}
		else:
			data["TOURELLE"] = None

		if self.BigEnemyBot is not None:
			system = self.BigEnemyBot
			data["BIGENEMYBOT"] = {}
			data["BIGENEMYBOT"]["getPosition"] = system.getPosition()
			data["BIGENEMYBOT"]["getRayon"] = system.getRayon()
		else:
			data["BIGENEMYBOT"] = None

		if self.SmallEnemyBot is not None:
			system = self.SmallEnemyBot
			data["SMALLENEMYBOT"] = {}
			data["SMALLENEMYBOT"]["getPosition"] = system.getPosition()
			data["SMALLENEMYBOT"]["getRayon"] = system.getRayon()
		else:
			data["SMALLENEMYBOT"] = None

		data["METADATA"] = {}
		data["METADATA"]["getOurColor"] = self.MetaData.getOurColor()
		data["METADATA"]["getGameClock"] = self.MetaData.getGameClock()
		return data
