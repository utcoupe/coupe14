# -*- coding: utf-8 -*-
"""
Système de récupèration de données des différants systèmes
"""

import threading
import time

#Cet objet crée un thread qui va récupère en permanence les données d'un système
class PullData():
	def __init__(self, constantes, objetCommunication, address):
		#Constantes
		self.pullPeriode = constantes.pullPeriode

		self.objetCommunication = objetCommunication

		#Variables


		#self.threadGestion = threading.Thread(target=self.gestion)
		#self.threadGestion.start()

	def gestion(self):
		time.sleep(self.pullPeriode/1000.0)
