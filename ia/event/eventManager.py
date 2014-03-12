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
	def __init__(self, Communication, Data):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__Communication = Communication
		self.__Flussmittel = Data.Flussmittel
		self.__Tibot = Data.Tibot
		self.__Tourelle = Data.Tourelle
		self.__MetaData = Data.MetaData

		self.__last_hokuyo_data = None

		self.__last_flussmittel_order_finished = ID_ACTION_MAX	#id_action
		self.__id_to_reach_flussmittel = 0
		self.__sleep_time_flussmittel = 0
		self.__resume_date_flussmittel = 0

		self.__last_tibot_order_finished = ID_ACTION_MAX			#id_action
		self.__id_to_reach_tibot = 0
		self.__sleep_time_tibot = 0
		self.__resume_date_tibot = 0

		self.__GoalsManager = goals.GoalsManager()

		self.__managerThread = threading.Thread(target=self.managerLoop)
		self.__managerThread .start()



	def managerLoop(self):
		#On attend le debut du match
		while self.__MetaData.getInGame() == False:
			#On defini l'id actuel de l'arduino comme point de debut, ça évite de devoir la reset
			if self.__Flussmittel is not None:
				self.__id_to_reach_flussmittel = self.__Flussmittel.getLastIdGlobale()
			else:
				self.__id_to_reach_flussmittel = 0
			
			if self.__Tibot is not None:
				self.__id_to_reach_tibot = self.__Tibot.getLastIdGlobale()
			else:
				self.__id_to_reach_tibot = 0
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#Pendant le match
		while self.__MetaData.getInGame() == True:
			self.__checkEvent()
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#On attend le debut de la funny action
		while self.__MetaData.getInFunnyAction() == False:
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#Pendant la funny action
		while self.__MetaData.getInFunnyAction() == True:
			#self.__checkEvent() ou fonction dédiée
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

	def __checkEvent(self):
		if self.__Tourelle is not None:
			new_data = ()
			if self.__Flussmittel is not None:
				new_data += (self.__Flussmittel.getPositon(),)
			if self.__Tibot is not None:
				new_data += (self.Tibot.getPositon(),)
			
			if new_data != self.__last_hokuyo_data:
				self.__last_hokuyo_data = new_data
				#TODO call collision

		if self.__Flussmittel is not None:
			new_id = self.__Flussmittel.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_flussmittel_order_finished:
				self.__last_flussmittel_order_finished = new_id

			#si on est sur l'action bloquante
			if self.__last_flussmittel_order_finished == self.__id_to_reach_flussmittel:
				#Gestion des sleep
				if self.__sleep_time_flussmittel > 0:
					self.__resume_date_flussmittel = int(time.time()*1000) + self.__sleep_time_flussmittel
					self.__sleep_time_flussmittel = 0
				else:
					#Si tu as attendu le SLEEP assez longtemps
					if int(time.time()*1000) > self.__resume_date_flussmittel:
						next_actions = self.__Flussmittel.getNextOrders()
						if next_actions is not None:
							self.__pushOrders(self.__Flussmittel, self.__Flussmittel.getNextOrders())
						else:
							self.__Flussmittel.setObjectifEnCours(None)


		if self.__Tibot is not None:
			new_id = self.__Tibot.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_tibot_order_finished:
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
						next_actions = self.__Tibot.getNextOrders()
						if next_actions is not None:
							self.__pushOrders(self.__Tibot, self.__Tibot.getNextOrders())
						else:
							self.__Tibot.setObjectifEnCours(None)

	def __pushOrders(self, Objet, data): 
		print("data" + str(data))
		id_objectif = data[0]
		Objet.setObjectifEnCours(id_objectif)
		data_action = data[1]#data_action est de type ((id_action, ordre, arguments),...)

		last_order = data_action.pop()
		if data_action:
			prev_last_order = data_action[-1]
			if Objet is self.__Flussmittel:
				print(self.__id_to_reach_flussmittel)
				self.__id_to_reach_flussmittel = prev_last_order[0]
				print(self.__id_to_reach_flussmittel)
			elif Objet is self.__Tibot:
				self.__id_to_reach_tibot = prev_last_order[0]
			else:
				self.__logger.error("Objet inconnu")


		if last_order[1] == 'SLEEP':
			if Objet is self.__Flussmittel:
				self.__sleep_time_flussmittel = last_order[2][0]
			elif Objet is self.__Tibot:
				self.__sleep_time_tibot = last_order[2][0]
			else:
				self.__logger.error("Objet inconnu")
		elif last_order[1] == 'END':
			#TODO call objectifManager
			pass
		elif last_order[1] == 'THEN':
			#Rien à faire
			pass
		else:
			self.__logger.error("ordre de stop impossible")

		self.__sendOrders((Objet.getAddressOther(), Objet.getAddressAsserv()), data_action)


	def __sendOrders(self, address, data_action):#data_action est de type ((id_action, ordre, arguments),...)
		#Si on est en jeuS
		if self.__MetaData.getInGame():
			for action in data_action:
				arg = [action[0]]
				#Si l'ordre a des arguments
				if action[2] is not None:
					arg += action[2]

				if action[1] == 'A_RESET_POS':#TODO enlever ce cas particulier, cet ordre doit avoir un id
					arg = []
					self.__Communication.sendOrderAPI(address[1], action[1], *arg)
				elif action[1][0] == 'O':
					self.__Communication.sendOrderAPI(address[0], action[1], *arg)
				elif action[1][0] == 'A':
					self.__Communication.sendOrderAPI(address[1], action[1], *arg)
				else:
					self.__logger.critical("L'ordre " + str(action[1]) + " ne suit pas la convention, il ne commence ni par A, ni par O")

				self.__logger.debug("Envoie des actions: " + str(action))
