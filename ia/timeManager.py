# -*- coding: utf-8 -*-
"""
Ce fichier attend le jack, arrete le robot à 90s et lance la funny action. Il simule aussi des evenement quand une action à besoin d'un sleep
"""

import time

from constantes import *

class TimeManager():
	def __init__(self, Communication, Data):
		self.__Communication = Communication
		self.__Flussmittel = Data.Flussmittel
		self.__Tibot = Data.Tibot
		self.__MetaData = Data.MetaData

		self.__date_match_begin = None
		self.__wait_dico = {}



	def startMatch(self):
		self.__MetaData.startMatch()
		self.__date_match_begin = int(time.time()*1000.0)

		#Pendant le match
		date_actuel = int(time.time()*1000.0)
		while( date_actuel - self.__date_match_begin ) < END_OF_MATCH:
			self.__MetaData.setGameClock(date_actuel - self.__date_match_begin)
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			date_actuel = int(time.time()*1000.0)

		self.__MetaData.stopMatch()
		self.__broadcastStopOrder()

		#Temps mort
		while ( date_actuel - self.__date_match_begin ) < BEGIN_FUNNY_ACTION:
			self.__MetaData.setGameClock(date_actuel - self.__date_match_begin)
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			date_actuel = int(time.time()*1000.0)

		#Pendant la funnyAction
		self.__MetaData.startFunny()
		date_actuel = int(time.time()*1000.0)
		while ( date_actuel - self.__date_match_begin ) < END_OF_FUNNY_ACTION:
			self.__MetaData.setGameClock(date_actuel - self.__date_match_begin)
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			date_actuel = int(time.time()*1000.0)

		self.__MetaData.stopFunny()
		self.__broadcastStopOrder()

	def __broadcastStopOrder(self):
		arg = []

		for i in range(1):#TODO augmenter le nombre de stop ?
			if self.__Flussmittel is not None:
				self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressAsserv(), 'A_CLEANG', *arg)#TODO quelle commande est utile et dans quelle ordre ?
				self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressAsserv(), 'A_KILLG', *arg)
			if self.__Tibot is not None:
				self.__Communication.sendOrderAPI(self.__Tibot.getAddressAsserv(), 'A_CLEANG', *arg)
				self.__Communication.sendOrderAPI(self.__Tibot.getAddressAsserv(), 'A_KILLG', *arg)
			time.sleep(100)

