# -*- coding: utf-8 -*-
"""
Classe globale pour toutes les données, on y instancie les objets
"""

import threading
import time

from . import ourBot
from . import enemyBot
from . import tourelle
from . import other

class Data():
	def __init__(self, communication, constantes, arduinoConstantes):
		self.constantes = constantes
		self.communication = communication
		self.system = {}

		self.flussmittel = ourBot.OurBot(constantes, communication, arduinoConstantes, 'ADDR_FLUSSMITTEL_OTHER', 'ADDR_FLUSSMITTEL_ASSERV', constantes.largeurFM, constantes.longueurFM)
		self.system['ADDR_FLUSSMITTEL_OTHER'] = self.flussmittel
		self.system['ADDR_FLUSSMITTEL_ASSERV'] = self.flussmittel

		self.tibot = ourBot.OurBot(constantes, communication, arduinoConstantes, 'ADDR_TIBOT_OTHER', 'ADDR_TIBOT_ASSERV', constantes.largeurTB, constantes.longueurTB)
		self.system['ADDR_TIBOT_OTHER'] = self.tibot
		self.system['ADDR_TIBOT_ASSERV'] = self.tibot

		if constantes.numberOfenemy >= 1:
			self.smallEnemyBot = enemyBot.EnemyBot(constantes, constantes.largeurBigEnemy, constantes.longueurBigEnemy)
		if constantes.numberOfenemy >= 2:
			self.bigEnemyBot = enemyBot.EnemyBot(constantes, constantes.largeurSmallEnemy, constantes.longueurSmallEnemy)

		self.tourelle = tourelle.Tourelle(constantes, communication, arduinoConstantes, 'ADDR_HOKUYO')
		self.system['ADDR_HOKUYO'] = self.tourelle

		self.other = other.Other(constantes)

		self.threadPull = threading.Thread(target=self.pullData)
		self.threadPull.start()


	def pullData(self):
		#Constantes
		pullPeriode = self.constantes.pullPeriode

		while True:
			orderTuple = self.communication.readOrdersAPI() # (address, order, arguments)

			if orderTuple != -1:
				address = orderTuple[0]
				order = orderTuple[1]
				arguments = orderTuple[2]

				if order == 'A_GET_POS':
					self.system[address].majPosition(arguments)

			time.sleep(pullPeriode/1000.0)
