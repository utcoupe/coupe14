# -*- coding: utf-8 -*-
"""
Classe qui recupère les données de tous les objets
"""

import threading 
import time

class PullData():
	def __init__(self, Communication, Flussmittel, Tibot, SmallEnemyBot, BigEnemyBot, Tourelle, PULL_PERIODE):
		self.Communication = Communication
		self.Flussmittel = Flussmittel[0]
		self.address_flussmittel_other = Flussmittel[1]
		self.address_flussmittel_asserv = Flussmittel[2]
		self.Tibot = Tibot[0]
		self.address_tibot_other = Tibot[1]
		self.address_tibot_asserv = Tibot[2]
		self.SmallEnemyBot = SmallEnemyBot
		self.BigEnemyBot = BigEnemyBot
		self.Tourelle = Tourelle[0]
		self.address_tourelle = Tourelle[1]
		self.PULL_PERIODE = PULL_PERIODE

		self.pull_data = True
		self.flussmittel_asked = False
		self.tibot_asked = False
		self.tourelle_asked = False

		self.ThreadPull = threading.Thread(target=self.gestion)
		self.ThreadPull.start()

	def gestion(self):
		while self.pull_data:
			self.readData()
			self.askData()
			time.sleep(self.PULL_PERIODE/1000.0)

	def stop(self):
		self.pull_data = False

	def askData(self):
		arguments = []
		if self.flussmittel_asked == False:
			if self.Flussmittel != None:
				self.Communication.sendOrderAPI(self.address_flussmittel_asserv, 'A_GET_POS', *arguments)
				self.flussmittel_asked = True

		if self.tibot_asked == False:
			if self.Tibot != None:
				self.Communication.sendOrderAPI(self.address_tibot_asserv, 'A_GET_POS', *arguments)
				self.tibot_asked = True

		if self.tourelle_asked == False:
			if self.Tourelle != None:
				self.Communication.sendOrderAPI(self.address_tourelle, 'GET_HOKUYO', *arguments)
				self.tourelle_asked = True


	def readData(self):
		orderTuple = self.Communication.readOrdersAPI() # (address, order, arguments)

		#Si on a un ordre à lire
		if orderTuple != -1:
			address = orderTuple[0]
			order = orderTuple[1]
			arguments = orderTuple[2]

			#Choix de l'objet
			if address == self.address_flussmittel_other or address == self.address_flussmittel_asserv:
				system = self.Flussmittel
				self.flussmittel_asked = False
			elif address == self.address_tibot_other or address == self.address_tibot_asserv:
				system = self.Tibot
				self.tibot_asked = False
			elif address == self.address_tourelle:
				system = self.Tourelle
				self.tourelle_asked = False
			else:
				system = None
				print("Erreur, un systeme non initilisé nous envoi des données")

			if system != None:
				if order == 'A_GET_POS':
					print("data:", arguments)
					system.majPosition(arguments)
				elif order == 'GET_HOKUYO':
					system.majPosition(arguments)
				elif order == 'GET_CAM':
					system.majCam(arguments)	
				else:
					print("Warning, ce retour n'est pas implementé, address", address, "ordre", order, "arguments", arguments)

			