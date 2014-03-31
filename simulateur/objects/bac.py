# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectPoly



class Bac(EngineObjectPoly):
	def __init__(self,engine,posinit,color):
		EngineObjectPoly.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_BAC,
			posinit			= posinit,
			mass			= MASS_INF,
			color			= color,
			poly_points		= map(lambda p: mm_to_px(*p),[(0,0),(700,0),(700,300-25),(0,300-25)])
		)
		self.nbFruit = 0

	def __repr__(self):
		return "Bac %s " % (self.posinit,)
