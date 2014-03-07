# -*- coding: utf-8 -*-
"""
Ce code gère l'envoi d'actions élémentaires aux robots et traite les collisions
"""

import threading
import time

from constantes import *

class EventManager():
	def __init__(self, Data):
		self.__Flussmitel = Data.Flussmittel
		self.__Tibot = Data.Tibot
		self.__Tourelle = Data.Tourelle
		self.__MetaData = Data.MetaData

		self.__last_hokuyo_data = None
		self.__last_flussmitel_order_finished = None	#id_action
		self.__id_to_reach_flussmitel = None
		self.__last_tibot_order_finished = None			#id_action
		self.__id_to_reach_tibot = None


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
			new_id = self.__Flussmitel.getLastIdOrderReceived()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_flussmitel_order_finished:
				self.__last_flussmitel_order_finished = new_id
				#si on a atteint 
				if self.__last_flussmitel_order_finished == self.__id_to_reach_flussmitel:
					self.pushOrders(self.__Flussmitel, self.__Flussmitel.getNextOrders())

		if self.__Tibot != None:
			new_id = self.__Tibot.getLastIdOrderReceived()
			print("id", new_id)
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_tibot_order_finished:
				self.__last_tibot_order_finished = new_id
				if self.__last_tibot_order_finished == self.__id_to_reach_tibot:
					self.pushOrders(self.__Tibot, self.__Tibot.getNextOrders())

	def pushOrders(self, objet, data_objectif): #data_objectif est de type ((id_action, ordre, arguments),...)
		last_order = data_objectif.pop()

		name = objet.getName()
		if name == 'FLUSSMITTEL':
			self.__last_flussmitel_order_finished = last_order[0] - 1
		elif name == 'TIBOT':
			self.__last_tibot_order_finished = last_order[0] - 1


		if last_order[1] == 'SLEEP':
			#TODO call time manager
			pass

		self.sendOrders(objet, data_objectif)


	def sendOrders(self, objet, orders):
		print("objet", objet, "orders", orders)
		#TODO call comm API
		