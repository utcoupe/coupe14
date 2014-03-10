# -*- coding: utf-8 -*-
"""
Ce fichier attend le jack, arrete le robot à 90s et lance la funny action. Il simule aussi des evenement quand une action à besoin d'un sleep
"""

import time

from constantes import *

class TimeManager():
	def __init__(self, MetaData):
		self.__MetaData = MetaData

		self.__date_match_begin = None


	def startMatch(self):
		self.__MetaData.startMatch()
		self.__date_match_begin = int(time.time()*1000.0)

		#Pendant le match
		dateActuel = int(time.time()*1000.0)
		while ( dateActuel - self.__date_match_begin ) < END_OF_MATCH:	
			self.__MetaData.setGameClock(dateActuel - self.__date_match_begin)
			#TODO gèrer les simulation d'event
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			dateActuel = int(time.time()*1000.0)

		self.__MetaData.stopMatch()
		#TODO broadcast stop

		#Temps mort
		while ( dateActuel - self.__date_match_begin ) < BEGIN_FUNNY_ACTION:	
			self.__MetaData.setGameClock(dateActuel - self.__date_match_begin)
			#TODO gèrer les simulation d'event
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			dateActuel = int(time.time()*1000.0)

		#Pendant la funnyAction
		self.__MetaData.startFunny()
		dateActuel = int(time.time()*1000.0)
		while ( dateActuel - self.__date_match_begin ) < END_OF_FUNNY_ACTION:	
			self.__MetaData.setGameClock(dateActuel - self.__date_match_begin)
			#TODO gèrer les simulation d'event
			time.sleep(PERIODE_TIME_MANAGER/1000.0)
			dateActuel = int(time.time()*1000.0)
		self.__MetaData.stopFunny()
		#TODO broadcast stop