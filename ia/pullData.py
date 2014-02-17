# -*- coding: utf-8 -*-
"""
Système de récupèration de données des différants systèmes
"""

import threading
import time

import classeRobots

class pullData():
	def __init__(self, objetCommunication):
		#Constantes
		self.nbEvent = 5 # nouvelle position FM, changement d'ordre FM, nouvelle position TB, changement d'ordre TB, nouvelles données hukuyo

		#Variables
		self.objetCommunication = objetCommunication
		self.indexLectureEvent = 0
		self.newEventArray = [False] * self.nbEvent

		self.threadGestion = threading.Thread(target=self.gestion)
		self.threadGestion.start()

	def gestion(self):
		while True:
			print("ok")
			time.sleep(5)
