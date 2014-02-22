# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""


class Tourelle():
	def __init__(self, constantes, communication, arduinoConstantes, address):
		self.communication = communication
		self.address = address
