# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""

from . import pullData

class tourelle():
	def __init__(self, communication):
		self.communication = communication