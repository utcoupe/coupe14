# -*- coding: utf-8 -*-
"""
Ce code gère l'envoi d'actions élémentaires aux robots et traite les collisions
"""

import threading
import logging
import time

from .constantes import *
from .subProcessCommunicate import *
from .navigation import *

class EventManager():
	def __init__(self, Communication, Data):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__Communication = Communication
		self.__Data = Data
		self.__Flussmittel = Data.Flussmittel
		self.__Tibot = Data.Tibot
		self.__SmallEnemyBot = Data.SmallEnemyBot
		self.__BigEnemyBot = Data.BigEnemyBot
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

		self.__SubProcessCommunicate = SubProcessCommunicate(Data)
		self.__Collision = Collision((self.__Flussmittel, self.__Tibot, self.__BigEnemyBot, self.__SmallEnemyBot))

		self.__managerThread = threading.Thread(target=self.__managerLoop)
		self.__managerThread.start()



	def __managerLoop(self):
		#On attend le debut du match
		while self.__MetaData.getInGame() == False:
			self.__majObjectif()
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#Pendant le match
		while self.__MetaData.getInGame() == True:
			self.__majObjectif()
			self.__checkEvent()
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#On attend le debut de la funny action
		while self.__MetaData.getInFunnyAction() == False:
			self.__majObjectif()
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

		#Pendant la funny action
		while self.__MetaData.getInFunnyAction() == True:
			self.__majObjectif() #TODO faire une fonction dédiée ?
			self.__checkEvent()
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

	def __majObjectif(self):
		"""Get new goals from objectifManager and add it to robot's goals queue"""
		new_data_list = self.__SubProcessCommunicate.readOrders()
		for new_data in new_data_list:
			nom_robot, id_prev_objectif, id_objectif, action_data = new_data

			if self.__Flussmittel is not None and nom_robot == self.__Flussmittel.getName():
				robot = self.__Flussmittel
			elif self.__Tibot is not None:
				robot = self.__Tibot
			else:
				robot = None

			if robot is not None:
				action_en_cours, objectif = robot.getQueuedObjectif()

				if objectif:
					last_objectif = objectif[-1]
				elif action_en_cours:
					last_objectif = action_en_cours
				else:
					last_objectif = robot.getLastIdObjectifExecuted()
				
				if last_objectif is not None:
					if last_objectif[0] == id_prev_objectif:
						robot.addNewObjectif(id_objectif, action_data)
					else:
						self.__logger.warning("On drop un nouvel ordre car il n'est pas à jour, id_prev_objectif: " + str(id_prev_objectif) + " last_objectif[0]: " + str(last_objectif[0]) + " action_data " + str(action_data))
				else:
					robot.addNewObjectif(id_objectif, action_data)

	def __checkEvent(self):
		self.__testCollision()
		if self.__Tourelle is not None:
			new_data = ()
			if self.__SmallEnemyBot is not None:
				new_data += (self.__SmallEnemyBot.getPositon(),)
			if self.__BigEnemyBot is not None:
				new_data += (self.__BigEnemyBot.getPositon(),)
			
			if new_data != self.__last_hokuyo_data:
				self.__last_hokuyo_data = new_data
				self.__testCollision()

		if self.__Flussmittel is not None:
			new_id = self.__Flussmittel.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_flussmittel_order_finished:
				self.__last_flussmittel_order_finished = new_id
				self.__Flussmittel.removeActionBellow(new_id)

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
							self.__pushOrders(self.__Flussmittel, next_actions)



		if self.__Tibot is not None:
			new_id = self.__Tibot.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_tibot_order_finished:
				self.__last_tibot_order_finished = new_id
				self.__Tibot.removeActionBellow(new_id)

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
							self.__pushOrders(self.__Tibot, next_actions)

	def __pushOrders(self, Objet, data): 
		print(str(Objet.getName()) + " charge les actions: " + str(data))
		id_objectif = data[0]
		data_action = data[1]#data_action est de type ((id_action, ordre, arguments),...)

		last_order = data_action.pop()
		if data_action:
			prev_last_order = data_action[-1]
			if Objet is self.__Flussmittel:
				self.__id_to_reach_flussmittel = prev_last_order[0]
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
			Objet.setLastIdObjectifExecuted(id_objectif)
			self.__SubProcessCommunicate.sendObjectifOver(id_objectif)
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

				if action[1][0] == 'O':
					self.__Communication.sendOrderAPI(address[0], action[1], *arg)
				elif action[1][0] == 'A':
					self.__Communication.sendOrderAPI(address[1], action[1], *arg)
				else:
					self.__logger.critical("L'ordre " + str(action[1]) + " ne suit pas la convention, il ne commence ni par A, ni par O")

				self.__logger.debug("Envoi de l'ordre: " + str(action))


	def __testCollision(self):
		if self.__Flussmittel is not None:
			collision_data = self.__Collision.getCollision(self.__Flussmittel)
			if collision_data is not None:
				self.__SubProcessCommunicate.sendObjectifCanceled(collision_data[0])

		if self.__Tibot is not None:
			collision_data = self.__Collision.getCollision(self.__Tibot)
			if collision_data is not None:
				self.__SubProcessCommunicate.sendObjectifCanceled(collision_data[0])


