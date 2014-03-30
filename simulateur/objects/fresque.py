# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectPoly



class Fresque(EngineObjectPoly):
	def __init__(self,engine,posinit):
		EngineObjectPoly.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_FRESQUE,
			posinit			= posinit,
			color			= "white",
			mass			= MASS_INF,
			poly_points		= map(lambda p: mm_to_px(*p),[(0,0),(600,0),(600,22),(0,22)])
		)
		self.objetsNous = 0
		self.objetsEnnemy = 0

	def __repr__(self):
		return "Fresque %s " % (self.posinit,)
