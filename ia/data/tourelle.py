# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""

from . import pullData

class Tourelle():
	def __init__(self, constantes, communication, arduinoConstantes, address):
		self.communication = communication
		self.address = address

		self.pullData = pullData.PullData(constantes, communication, self.address)