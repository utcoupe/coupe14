# -*- coding: utf-8 -*-
"""
Ce fichier attend le jack, arrete le robot à 90s et lance la funny action. Il simule aussi des evenement quand une action à besoin d'un sleep
"""

import time
import logging

from constantes import *

class TimeManager():
	def __init__(self, Communication, Data):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__Communication = Communication
		self.__Flussmittel = Data.Flussmittel
		self.__Tibot = Data.Tibot
		self.__MetaData = Data.MetaData

		self.__date_match_begin = None
		self.__wait_dico = {}

		self.__sendResetBot()
		Data.startPullData()



	def startMatch(self):
		self.__date_match_begin = int(time.time()*1000.0)
		self.__logger.info("On commence le match !")

		#Pendant le match
		date_actuel = int(time.time()*1000.0)
		while( date_actuel - self.__date_match_begin ) < END_OF_MATCH:
			self.__MetaData.setGameClock(date_actuel - self.__date_match_begin)
			if ( date_actuel - self.__date_match_begin ) > BEGIN_CHECK_COLLISION and self.__MetaData.getCheckCollision() == False:
				self.__MetaData.startCheckCollision()
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			date_actuel = int(time.time()*1000.0)

		self.__MetaData.stopMatch()
		self.__broadcastStopOrder()
		self.__logger.info("On a terminé le match après "+str(self.__MetaData.getGameClock())+" ms de jeu")

		#Temps mort
		while ( date_actuel - self.__date_match_begin ) < BEGIN_FUNNY_ACTION:
			self.__MetaData.setGameClock(date_actuel - self.__date_match_begin)
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			date_actuel = int(time.time()*1000.0)

		self.__logger.info("On a terminé l'attente de Funny_action après "+str(self.__MetaData.getGameClock())+" ms de jeu")

		#Pendant la funnyAction
		self.__MetaData.startFunny()
		date_actuel = int(time.time()*1000.0)
		while ( date_actuel - self.__date_match_begin ) < END_OF_FUNNY_ACTION:
			self.__MetaData.setGameClock(date_actuel - self.__date_match_begin)
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			date_actuel = int(time.time()*1000.0)

		self.__MetaData.stopFunny()
		self.__broadcastStopOrder()
		self.__logger.info("On a terminé l'attente la Funny_action après "+str(self.__MetaData.getGameClock())+" ms de jeu")

	def __broadcastStopOrder(self):
		empty_arg = []

		if self.__Flussmittel is not None:
			self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressAsserv(), 'PAUSE', *empty_arg)
			self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressOther(), 'PAUSE', *empty_arg)

		if self.__Tibot is not None:
			self.__Communication.sendOrderAPI(self.__Tibot.getAddressAsserv(), 'PAUSE', *empty_arg)
			self.__Communication.sendOrderAPI(self.__Tibot.getAddressOther(), 'PAUSE', *empty_arg)

		self.__logger.info("On arrete les robtos avec broadcastStopOrder")

	def __sendResetBot(self):
		empty_arg = []

		if self.__Flussmittel is not None:
			position_arg = self.__MetaData.getFirstPositionFlussmittel()
			if position_arg is None:
				self.__logger.error("On a pas initialisé la position de Flussmittel")
			self.__Flussmittel.setPosition(position_arg[0], position_arg[1], position_arg[2])
			self.__Communication.sendOrderAPI(self.__Flussmittel.getAddressAsserv(), 'A_SET_POS', *position_arg)


		if self.__Tibot is not None:
			position_arg = self.__MetaData.getFirstPositionTibot()
			if position_arg is None:
				self.__logger.error("On a pas initialisé la position de Tibot")
			self.__Tibot.setPosition(position_arg[0], position_arg[1], position_arg[2])
			self.__Communication.sendOrderAPI(self.__Tibot.getAddressAsserv(), 'A_SET_POS', *position_arg)


