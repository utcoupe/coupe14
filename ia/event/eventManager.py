# -*- coding: utf-8 -*-
"""
Ce code gère l'envoi d'actions élémentaires aux robots et traite les collisions
"""

import threading
import logging
import time

from . import goals
from .constantes import *

class EventManager():
	def __init__(self, Communication, TimeManager, Data):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__Communication = Communication
		self.__TimeManager = TimeManager
		self.__Flussmitel = Data.Flussmittel
		self.__Tibot = Data.Tibot
		self.__Tourelle = Data.Tourelle
		self.__MetaData = Data.MetaData

		self.__last_hokuyo_data = None
		self.__last_flussmitel_order_finished = 29999	#id_action
		self.__id_to_reach_flussmitel = 0
		self.__sleep_time_flussmitel = 0
		self.__resume_date_flussmittel = 0

		self.__last_tibot_order_finished = 29999			#id_action
		self.__id_to_reach_tibot = 0
		self.__sleep_time_tibot = 0
		self.__resume_date_tibot = 0

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
		if self.__Tourelle is not None:
			new_data = self.__Tourelle.getLastDataPosition()
			if new_data != self.__last_hokuyo_data:
				self.__last_hokuyo_data = new_data
				#TODO call collision

		if self.__Flussmitel is not None:
			new_id = self.__Flussmitel.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_flussmitel_order_finished:
				self.__last_flussmitel_order_finished = new_id

			#si on est sur l'action bloquante
			if self.__last_flussmitel_order_finished == self.__id_to_reach_flussmitel:
				#Gestion des sleep
				if self.__sleep_time_flussmitel > 0:
					self.__resume_date_flussmittel = int(time.time()*1000) + self.__sleep_time_flussmitel
					self.__sleep_time_flussmitel = 0
				else:
					#Si tu as attendu le SLEEP assez longtemps
					if int(time.time()*1000) > self.__resume_date_flussmittel:
						self.pushOrders(self.__Flussmitel, self.__Flussmitel.getNextOrders())


		if self.__Tibot is not None:
			new_id = self.__Tibot.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_tibot_order_finished:
				print("Debug: Tibot vient de finir la commande d'id: " + str(new_id))
				self.__last_tibot_order_finished = new_id

			#si on est sur l'action bloquante
			if self.__last_tibot_order_finished == self.__id_to_reach_tibot:
				#Gestion des sleep
				if self.__sleep_time_tibot > 0:
					self.__resume_date_tibot = int(time.time()*1000) + self.__sleep_time_tibot
					self.__sleep_time_tibot = 0
				else:
					#Si tu as attendu le SLEEP assez longtemps
					if int(time.time()*1000) > self.__resume_date_tibot:
						self.pushOrders(self.__Tibot, self.__Tibot.getNextOrders())

	def pushOrders(self, objet, data): 
		print("data: " + str(data))
		id_objectif = data[0]
		data_action = data[1]#data_action est de type ((id_action, ordre, arguments),...)

		last_order = data_action.pop()
		if data_action:
			prev_last_order = data_action[-1]
			if objet is self.__Flussmitel:
				self.__id_to_reach_flussmitel = prev_last_order[0]
			elif objet is self.__Tibot:
				self.__id_to_reach_tibot = prev_last_order[0]
			else:
				self.__logger.error("objet inconnu")


		if last_order[1] == 'SLEEP':
			print("debug ttstb:" + str(last_order[2][0]))
			if objet is self.__Flussmitel:
				self.__sleep_time_flussmitel = last_order[2][0]
			elif objet is self.__Tibot:
				self.__sleep_time_tibot = last_order[2][0]
			else:
				self.__logger.error("objet inconnu")

		elif last_order[1] == 'END':
			#TODO call objectifManager
			pass

		elif last_order[1] == 'THEN':
			#Rien à faire
			pass

		else:
			self.__logger.error("ordre de stop impossible")

		self.__sendOrders((objet.getAddressOther(), objet.getAddressAsserv()), data_action)


	def __sendOrders(self, address, data_action):#data_action est de type ((id_action, ordre, arguments),...)
		for action in data_action:
			arg = [action[0]]
			if action[2] is not None:
				arg += action[2]
			print(arg)
			if action[1][0] == 'O':
				self.__Communication.sendOrderAPI(address[0], action[1], *arg)
			elif action[1][0] == 'A':
				self.__Communication.sendOrderAPI(address[1], action[1], *arg)
			else:
				self.__logger.critical("L'ordre " + action[1] + " ne suit pas la convention, il ne commence ni par A, ni par O")
			print("Debug: envoie de action:" + str(action))
