# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectCircle



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
		self.feu = 3

	def __repr__(self):
		return "Torche %s " % (self.posinit,)