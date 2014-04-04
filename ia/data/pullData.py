# -*- coding: utf-8 -*-
"""
Classe qui recupère les données de tous les objets
"""

import threading 
import time
import logging

class PullData():
	def __init__(self, Communication, Flussmittel, Tibot, SmallEnemyBot, BigEnemyBot, ComputeHokuyoData, Tourelle, PULL_PERIODE):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.Communication = Communication
		self.Flussmittel = Flussmittel[0]
		self.address_flussmittel_other = Flussmittel[1]
		self.address_flussmittel_asserv = Flussmittel[2]
		self.Tibot = Tibot[0]
		self.address_tibot_other = Tibot[1]
		self.address_tibot_asserv = Tibot[2]
		self.SmallEnemyBot = SmallEnemyBot
		self.BigEnemyBot = BigEnemyBot
		self.ComputeHokuyoData = ComputeHokuyoData
		self.Tourelle = Tourelle[0]
		self.address_tourelle = Tourelle[1]
		self.PULL_PERIODE = PULL_PERIODE

		self.__pull_data = True
		self.__id_flussmittel_other_asked = False
		self.__data_flussmittel_asserv_asked = False
		self.__id_tibot_other_asked = False
		self.__data_tibot_asserv_asked = False
		self.tourelle_asked = False

		self.__ThreadPull = threading.Thread(target=self.__gestion)

	def start(self):
		self.__ThreadPull.start()

	def stop(self):
		"""méthode public pour arreter le système de pull data"""
		self.__pull_data = False

	def __gestion(self):
		while self.__pull_data:
			self.__readData()
			self.__askData()
			time.sleep(self.PULL_PERIODE/1000.0)

	def __askData(self):
		arguments = []

		if self.Flussmittel is not None:
			if self.__id_flussmittel_other_asked == False:
				self.Communication.sendOrderAPI(self.address_flussmittel_other, 'GET_LAST_ID', *arguments)
				self.__id_flussmittel_other_asked = True

			if self.__data_flussmittel_asserv_asked == False:
				self.Communication.sendOrderAPI(self.address_flussmittel_asserv, 'A_GET_POS_ID', *arguments)
				self.__data_flussmittel_asserv_asked = True

		if self.Tibot is not None:
			if self.__id_tibot_other_asked == False:
				self.Communication.sendOrderAPI(self.address_tibot_other, 'GET_LAST_ID', *arguments)
				self.__id_tibot_other_asked = True

			if self.__data_tibot_asserv_asked == False:
				self.Communication.sendOrderAPI(self.address_tibot_asserv, 'A_GET_POS_ID', *arguments)
				self.__data_tibot_asserv_asked = True
				
		if self.Tourelle is not None:
			if self.tourelle_asked == False:
				self.Communication.sendOrderAPI(self.address_tourelle, 'GET_HOKUYO', *arguments)
				self.tourelle_asked = True


		#Hokuyo Fictif
		self.Tourelle.majPosition(generateFictionHokuyo());


	def __readData(self):
		orderTuple = self.Communication.readOrdersAPI() # (address, order, arguments)

		#Si on a un ordre à lire
		if orderTuple != -1:
			address = orderTuple[0]
			order = orderTuple[1]
			arguments = orderTuple[2]

			#Choix de l'objet
			if address == self.address_flussmittel_other:
				system = self.Flussmittel
				if order == 'GET_LAST_ID':
					self.__id_flussmittel_other_asked = False

			elif address == self.address_flussmittel_asserv:
				system = self.Flussmittel
				if order == 'A_GET_POS_ID':
					self.__data_flussmittel_asserv_asked = False

			elif address == self.address_tibot_other:
				system = self.Tibot
				if order == 'GET_LAST_ID':
					self.__id_tibot_other_asked = False

			elif address == self.address_tibot_asserv:
				system = self.Tibot
				if order == 'A_GET_POS_ID':
					self.__data_tibot_asserv_asked = False
					
			elif address == self.address_tourelle:
				system = self.Tourelle
				self.tourelle_asked = False
			else:
				system = None
				self.__logger.error("un systeme non initilisé nous envoi des données")

			if system is not None:
				if order == 'A_GET_POS_ID':
					system.setPositionAndId(address, arguments)
				elif order == 'GET_LAST_ID':
					system.setLastId(address, arguments[0])
				elif order == 'GET_HOKUYO':
					system.majPosition(arguments)
				elif order == 'GET_CAM':
					system.majCam(arguments)
				elif order == 'A_GOTO':
					pass	
				else:
					self.__logger.warning("ce retour n'est pas implementé, address " + str(address) + " ordre " + str(order) + " arguments " + str(arguments))

			



def generateFictionHokuyo():
	nombreRobots = 4				#Max:4
	centre = {"x":1500, "y":1000}	#mm
	amplitudeX = 800				#mm
	amplitudeY = 300				#mm


	import math
	ret = [generateFictionHokuyo.iteration*100]
	angle = (generateFictionHokuyo.iteration%100)*math.pi/50 #un tour toutes les 10s -> 100 iterations

	for i in range(nombreRobots):
		currAngle = angle+ i*2*math.pi/nombreRobots
		ret.append(int(centre["x"] + math.cos(currAngle)*amplitudeX))
		ret.append(int(centre["y"] + math.sin(currAngle)*amplitudeY))
	for i in range(nombreRobots, 4):
		ret.append(0)
		ret.append(0)

	generateFictionHokuyo.iteration += 1
	return ret
generateFictionHokuyo.iteration = 0


