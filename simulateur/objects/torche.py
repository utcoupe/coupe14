# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectCircle
import time

class Torche(EngineObjectCircle):
	def __init__(self,engine,posinit):
		EngineObjectCircle.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_TORCHE,
			posinit			= posinit,
			color			= "brown",
			mass 			= 500,
			radius			= mm_to_px(80)
		)
		self.__nbr_feu = 3
		self.__ordre_feu = []
		if posinit[0] == 225:
			#print('torche rouge')
			self.__ordre_feu = ['R','Y','R']
		elif posinit[0] == 525:
			#print('torche jaune')
			self.__ordre_feu = ['Y','R','Y']

	def prendreFeu(self):
		if self.__nbr_feu > 0:
			self.__nbr_feu -= 1
			feu = self.__ordre_feu.pop()
		else:
			feu = None
		return feu

	def __repr__(self):
		return "Torche %s " % (self.posinit,)