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

		self.__broadcastStopOrder()
		self.__sendResetBot()
		Data.startPullData()



	def startMatch(self):
		self.__MetaData.startMatch()
		self.__date_match_begin = int(time.time()*1000.0)

		#Pendant le match
		date_actuel = int(time.time()*1000.0)
		while( date_actuel - self.__date_match_begin ) < END_OF_MATCH:
			self.__MetaData.setGameClock(date_actuel - self.__date_match_begin)
			if ( date_actuel - self.__date_match_begin ) > BEGIN_CHECK_COLLISION:
				self.__MetaData.startCheckCollision()
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
				self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressAsserv(), 'A_CLEANG', *arg)
			if self.__Tibot is not None:
				self.__Communication.sendOrderAPI(self.__Tibot.getAddressAsserv(), 'A_CLEANG', *arg)
			time.sleep(0.05)

	def __sendResetBot(self):
		arg = []

		if self.__Flussmittel is not None:
			self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressAsserv(), 'A_RESET_POS', *arg)
			self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressAsserv(), 'RESET_ID', *arg)
			self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressOther() , 'RESET_ID', *arg)
		if self.__Tibot is not None:
			self.__Communication.sendOrderAPI(self.__Tibot.getAddressAsserv(), 'A_RESET_POS', *arg)
			self.__Communication.sendOrderAPI(self.__Tibot.getAddressAsserv(), 'RESET_ID', *arg)
			self.__Communication.sendOrderAPI(self.__Tibot.getAddressOther() , 'RESET_ID', *arg)

