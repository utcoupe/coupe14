# -*- coding: utf-8 -*-
"""
Ce code gère l'envoi d'actions élémentaires aux robots et traite les collisions
"""

import threading
import time
import os

from constantes import *
import goals
import logging

class EventManager():
	def __init__(self, Communication, Data):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__Communication = Communication
		self.__Flussmitel = Data.Flussmittel
		self.__Tibot = Data.Tibot
		self.__Tourelle = Data.Tourelle
		self.__MetaData = Data.MetaData

		self.__last_hokuyo_data = None
		self.__last_flussmitel_order_finished = -1	#id_action
		self.__id_to_reach_flussmitel = 0
		self.__last_tibot_order_finished = -1			#id_action
		self.__id_to_reach_tibot = 0

		self.__GoalsManager = goals.GoalsManager()

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
		if self.__Tourelle != None:
			new_data = self.__Tourelle.getLastDataPosition()
			if new_data != self.__last_hokuyo_data:
				self.__last_hokuyo_data = new_data
				#TODO call collision

		if self.__Flussmitel != None:
			new_id = self.__Flussmitel.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_flussmitel_order_finished:
				self.__last_flussmitel_order_finished = new_id
				#si on a atteint l'action bloquante
				if self.__last_flussmitel_order_finished == self.__id_to_reach_flussmitel:
					self.pushOrders(self.__Flussmitel, self.__Flussmitel.getNextOrders())

		if self.__Tibot != None:
			new_id = self.__Tibot.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_tibot_order_finished:
				print("id", new_id)
				self.__last_tibot_order_finished = new_id
				#si on a atteint l'action bloquante
				if self.__last_tibot_order_finished == self.__id_to_reach_tibot:
					self.pushOrders(self.__Tibot, self.__Tibot.getNextOrders())

	def pushOrders(self, objet, data): 
		id_objectif = data[0]
		data_action = data[1]#data_action est de type ((id_action, ordre, arguments),...)

		last_order = data_action.pop()
		if len(data_action) > 0:
			prev_last_order = data_action[-1]
			name = objet.getName()
			if name == 'FLUSSMITTEL':
				self.__id_to_reach_flussmitel = prev_last_order[0]
			elif name == 'TIBOT':
				self.__id_to_reach_tibot = prev_last_order[0]


		if last_order[1] == 'SLEEP':
			#TODO call time manager
			pass
		elif last_order[1] == 'END':
			#TODO call objectifManager
			pass

		self.sendOrders((objet.getAddressOther(), objet.getAddressAsserv()), data_action)


	def sendOrders(self, address, data_action):#data_action est de type ((id_action, ordre, arguments),...)
		for action in data_action:
			arg = list(map(int, list(action[0]) + action[2].split(',')))
			print(arg)
			if action[1][0] == 'O':
				self.__Communication.sendOrderAPI(address[0], action[1], *arg)
			elif action[1][0] == 'A':
				self.__Communication.sendOrderAPI(address[1], action[1], *arg)
			else:
				self.__logger.critical("L'ordre " + action[1] + " ne suit pas la convention, il ne commence ni par A, ni par O")
			print("envoie de action:" + str(action))

		