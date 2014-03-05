# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""

from constantes import *

class Tourelle():
	def __init__(self, communication, arduinoConstantes, address):
		self.__communication = communication
		self.__address = address

		#Variables
		

	#utilise les données en provenance des tourelles pour mettre à jour les données de la classe
	def majPosition(self, arguments):
		pass
		#TODO
