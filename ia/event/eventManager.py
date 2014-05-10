# -*- coding: utf-8 -*-
"""
Ce code gère l'envoi d'actions élémentaires aux robots et traite les collisions
"""

import threading
import logging
import time
import os
import sys


from .constantes import *
from .subProcessCommunicate import *
from .collision import *

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
		self.__tibot_locked = False
		self.__filet_fired = False

		self.__last_flussmittel_order_finished = ID_ACTION_MAX	#id_action
		self.__sleep_time_flussmittel = 0
		self.__resume_date_flussmittel = 0

		self.__last_tibot_order_finished = ID_ACTION_MAX			#id_action
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
			if self.__filet_fired == False:
				empty_arg = [42,]# 42 est un nombre aleatoire
				self.__Communication.sendOrderAPI("ADDR_TIBOT_OTHER", "O_TIR_FILET", *empty_arg)
				self.__logger.info("On lance le filet")
				self.__filet_fired = True
			time.sleep(PERIODE_EVENT_MANAGER/1000.0)

	def __majObjectif(self):
		"""Get new goals from objectifManager and add it to robot's goals queue"""
		new_data_list = self.__SubProcessCommunicate.readOrders()
		for new_data in new_data_list:

			if new_data[0] == "add":
				nom_robot, id_prev_objectif, id_objectif, action_data = new_data[1]
				robot = self.__getSystem(nom_robot)

				if robot == self.__Flussmittel:
					self.__SubProcessCommunicate.sendTibotGoalManagerObjectifBlocked(id_objectif)
				else:
					self.__SubProcessCommunicate.sendFlussmittelGoalManagerObjectifBlocked(id_objectif)

				action_en_cours, objectif = robot.getQueuedObjectif()
				added = False

				#stacking normale
				if objectif:
					last_id_objectif = objectif[-1][0]
				elif action_en_cours:
					last_id_objectif = action_en_cours[0]
				else:
					last_id_objectif = robot.getLastIdObjectifExecuted()
				
				if last_id_objectif is not None:
					if id_prev_objectif == last_id_objectif:
						robot.addNewObjectif(id_objectif, action_data)
						added = True
				else:#cas spéciale du premier ordre
					robot.addNewObjectif(id_objectif, action_data)
					added = True

				if added == False:
					self.__logger.warning(str(nom_robot)+" On drop un nouvel ordre car il n'est pas à jour, on a reçu id_prev_objectif: " + str(id_prev_objectif) + " on attendait last_id_objectif: " + str(last_id_objectif) + " action_data " + str(action_data))
					self.__SubProcessCommunicate.sendObjectifsCanceled((id_objectif,))


			elif new_data[0] == "step":
				nom_robot, id_prev_objectif, id_objectif, action_data = new_data[1]
				robot = self.__getSystem(nom_robot)
				robot.addOrderStepOver(id_objectif, action_data)

			elif new_data[0] == "delete":
				nom_robot = new_data[1]
				robot = self.__getSystem(nom_robot)
				id_objectif_to_remove = new_data[2]

				robot.deleteObjectifInStepOver(id_objectif_to_remove)
				robot.setIdToReach("ANY")

			else:
				self.__logger.critical("La fonction demandé n'est pas implementé, new_data "+str(new_data))

	def __getSystem(self, nom_robot):
		#On voit quel système est concerné
		if self.__Flussmittel is not None and nom_robot == self.__Flussmittel.getName():
			robot = self.__Flussmittel
		elif self.__Tibot is not None:
			robot = self.__Tibot
		else:
			robot = None
			self.logger.critical(str(nom_robot)+" on a reçu un ordre pour un robot qui n'existe pas")
		return robot

	def __checkEvent(self):
		self.__checkBrasStatus()

		if self.__Tourelle is not None:
			new_data = ()
			if self.__BigEnemyBot is not None:
				new_data += (self.__BigEnemyBot.getPosition(),)
			if self.__SmallEnemyBot is not None:
				new_data += (self.__SmallEnemyBot.getPosition(),)
			
			if new_data != self.__last_hokuyo_data:
				self.__last_hokuyo_data = new_data
				if self.__MetaData.getCheckCollision():
					self.__testCollision()

		if self.__Flussmittel is not None:
			new_id = self.__Flussmittel.getLastIdGlobale()
			#si un nouvel ordre s'est terminé
			if new_id != self.__last_flussmittel_order_finished:
				self.__last_flussmittel_order_finished = new_id
				self.__Flussmittel.removeActionBellow(new_id)

			#si on est sur l'action bloquante
			if self.__last_flussmittel_order_finished == self.__Flussmittel.getIdToReach() or self.__Flussmittel.getIdToReach() == "ANY":
				#Gestion des sleep
				if self.__sleep_time_flussmittel > 0:
					self.__resume_date_flussmittel = int(time.time()*1000) + self.__sleep_time_flussmittel
					self.__sleep_time_flussmittel = 0
				else:
					#Si tu as attendu le SLEEP assez longtemps
					if int(time.time()*1000) > self.__resume_date_flussmittel:
						if self.__Flussmittel.getFinEnCours():
							self.__Flussmittel.setFinEnCours(False)
							self.__SubProcessCommunicate.sendObjectifOver(self.__Flussmittel.getLastIdObjectifExecuted())
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
			if self.__last_tibot_order_finished == self.__Tibot.getIdToReach() or self.__Tibot.getIdToReach() == "ANY":
				#Gestion des sleep
				if self.__sleep_time_tibot > 0:
					self.__resume_date_tibot = int(time.time()*1000) + self.__sleep_time_tibot
					self.__sleep_time_tibot = 0
				else:
					#Si tu as attendu le SLEEP assez longtemps
					if int(time.time()*1000) > self.__resume_date_tibot:
						if self.__Tibot.getFinEnCours():
							self.__Tibot.setFinEnCours(False)
							self.__SubProcessCommunicate.sendObjectifOver(self.__Tibot.getLastIdObjectifExecuted())
						next_actions = self.__Tibot.getNextOrders()
						if next_actions is not None:
							self.__pushOrders(self.__Tibot, next_actions)

	def __checkBrasStatus(self):
		if self.__Flussmittel is not None:
			bras_status = self.__Flussmittel.getBrasStatus()
			if bras_status is not None:
				self.__Flussmittel.setBrasStatus(None)
				self.__SubProcessCommunicate.sendBrasStatus(bras_status, self.__Flussmittel.getQueuedObjectif()[1][0][0])

	def __pushOrders(self, Objet, data): 
		id_objectif = data[0]
		data_action_temp = data[1]#data_action est de type ((fack_id_action, ordre, arguments),...)

		data_action = deque()
		#Set vrai id
		for action in data_action_temp:
			data_action.append((Objet.getNextIdToStack(), action[1], action[2]))

		print(str(Objet.getName()) + " charge les actions dans eventManager: " + str((id_objectif, data_action)))

		last_order = data_action.pop()
		if data_action:
			prev_last_order = data_action[-1]
			if Objet is self.__Flussmittel:
				self.__Flussmittel.setIdToReach(prev_last_order[0])
			elif Objet is self.__Tibot:
				self.__Tibot.setIdToReach(prev_last_order[0])
			else:
				self.__logger.error("Objet inconnu")

		if last_order[1] == 'SLEEP':
			if Objet is self.__Flussmittel:
				self.__sleep_time_flussmittel = last_order[2][0]
			elif Objet is self.__Tibot:
				self.__sleep_time_tibot = last_order[2][0]
			else:
				self.__logger.error("Objet inconnu")

		elif last_order[1] == 'STEP_OVER':
			self.__SubProcessCommunicate.sendObjectifStepOver(id_objectif)

		elif last_order[1] == 'END':
			Objet.setLastIdObjectifExecuted(id_objectif)
			Objet.setFinEnCours(True)

		elif last_order[1] == 'DYNAMIQUE_OVER':
			self.__SubProcessCommunicate.sendObjectifDynamiqueOver(id_objectif)

		elif last_order[1] == 'THEN' or last_order[1] == 'END_GOTO':
			#Rien à faire
			pass

		else:
			self.__logger.error("ordre de stop impossible, last_order"+str(last_order))

		self.__sendOrders((Objet.getAddressOther(), Objet.getAddressAsserv()), Objet, data_action, id_objectif)


	def __sendOrders(self, address, Objet, data_action, id_objectif):#data_action est de type ((id_action, ordre, arguments),...)
		#Si on est en jeu
		if self.__MetaData.getInGame():
			for action in data_action:
				arg = [action[0]]
				
				#Si l'ordre a des arguments
				if action[2] is not None:
					arg += action[2]

				if action[1][0] == 'O':
						if self.__tibot_locked == False:
							self.__Communication.sendOrderAPI(address[0], action[1], *arg)
						else:
							self.__logger.error("Attention on drop l'ordre "+str(action[1])+" a destination de "+str(address[0])+" avec les arg "+str(arg)+" car on est bloqué en funny action.")

				elif action[1][0] == 'A':
					if action[1] == "A_GOTO_SCRIPT":#A_GOTO_SCRIPT n'existe que dans les scripts d'action elemetaire, on l'utilise pour ne pas inclure ces deplacements dans le calcul de collision
						self.__Communication.sendOrderAPI(address[1], "A_GOTO", *arg)
					else:
						self.__Communication.sendOrderAPI(address[1], action[1], *arg)

				elif action[1] == "FUNNY_ACTION_LOCK":
					self.__tibot_locked = True
					self.__logger.info("Tibot est prêt pour la funny action, il ne bougera plus.")

				else:
					self.__logger.critical("L'ordre " + str(action[1]) + " ne suit pas la convention, il ne commence ni par A, ni par O")

				self.__logger.debug(str(address) + " envoi de l'ordre: " + str(action))


	def __testCollision(self):
		if self.__Flussmittel is not None:
			self.__checkSystem(self.__Flussmittel)
		
		if self.__Tibot is not None:
			self.__checkSystem(self.__Tibot)
	
	def __checkSystem(self, system):
		collision_data = self.__Collision.getCollision(system)
		if collision_data is not None:
			distance = collision_data[1]
			if distance < self.__MetaData.getCollisionThreshold():
				first_id_to_remove = collision_data[0]
				id_canceled_list = system.removeObjectifAbove(first_id_to_remove)
				self.__logger.info("On annule les ordres: " + str(id_canceled_list) + " pour causes de collision dans " + str(distance) + " mm")
				empty_arg = []
				self.__Communication.sendOrderAPI(system.getAddressAsserv(), 'A_CLEANG', *empty_arg)
				system.setIdToReach("ANY")
				self.__SubProcessCommunicate.sendObjectifsCanceled(id_canceled_list)
			else:
				self.__logger.debug("On a detecté une collision dans "+str(distance)+" mm, mais on continue")
