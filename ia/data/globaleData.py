# -*- coding: utf-8 -*-
"""
Classe globale pour toutes les données, on y instancie les objets
"""

from . import ourBot
from . import ennemyBot
from . import tourelle
from . import other

class data():
	def __init__(self):
		self.FM = ourBot.ourBot()
