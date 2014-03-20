# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""

from .dataStructure import *
from constantes import *

class Tourelle():
	def __init__(self, Flussmittel, Tibot, BigEnemyBot, SmallEnemyBot, communication, arduinoConstantes, address):
		self.Flussmittel = Flussmittel
		self.Tibot = Tibot
		self.BigEnemyBot = BigEnemyBot
		self.SmallEnemyBot = SmallEnemyBot
		self.__communication = communication
		self.__address = address

		#Variables
		self.__last_data_position = None
		
	
	def getLastDataPosition(self):
		return self.__last_data_position

	def majPosition(self, arguments):
		timestamp = arguments[0]

		position_nos_robots = []
		if self.Flussmittel is not None:
			temp = self.Flussmittel.getPositon
			position_nos_robots.append(dataStructure.Position(temp[0], temp[0]))

		if self.Tibot is not None:
			temp = self.Tibot.getPositon
			position_nos_robots.append(dataStructure.Position(temp[0], temp[0]))

		position_hokuyo = []
		for i in range(1,9,2):
			if arguments[i] == -1 and arguments[i+1] == -1:
				break
			position_hokuyo.append(arguments[i], arguments[i+1])

		self.__tracking(timestamp, position_nos_robots, position_hokuyo)

	def __tracking(self, timestamp, position_nos_robots, position_hokuyo):
		#TODO traitement pour suivi des robots ici
		#self.Tourelle.setFormatedPosition(position_big_enemy, position_small_enemy)
		pass

	def __setFormatedPosition(self, position_big_enemy, position_small_enemy):
		"""Cette méthode ne doit être appelé qu'avec des données formatées par data/computeHokuyoData.py"""
		pass
		#TODO