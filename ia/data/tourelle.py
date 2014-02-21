# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""

from . import pullData

class Tourelle():
	def __init__(self, communication):
		self.communication = communication
		self.pullData = pullData.PullData(communication)