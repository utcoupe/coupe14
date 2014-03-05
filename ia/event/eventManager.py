# -*- coding: utf-8 -*-
"""
Ce code gère l'envoi d'actions élémentaires aux robots et traite les collisions
"""

import threading
import time

from constantes import *

class EventManager():
	def __init__(self, MetaData):
		self.__MetaData = MetaData
		self.__managerThread = threading.Thread(target=self.managerLoop)
		self.__managerThread .start()

	def managerLoop(self):
		#On attend le debut du match
		while self.__MetaData.getInGame() == False:
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#Pendant le match
		while self.__MetaData.getInGame() == True:
			self.checkEvent()
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#On attend le debut de la funny action
		while self.__MetaData.getInFunnyAction() == False:
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#Pendant la funny action
		while self.__MetaData.getInFunnyAction() == True:
			self.checkEvent()
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

	def checkEvent(self):
		print(self.__MetaData.getGameClock(), self.__MetaData.getInGame(), self.__MetaData.getInFunnyAction())