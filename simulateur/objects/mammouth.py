# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectPoly



class Mammouth(EngineObjectPoly):
	def __init__(self,engine,posinit):
		EngineObjectPoly.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_MAMMOUTH,
			posinit			= posinit,
			color			= "brown",
			mass			= MASS_INF,
			poly_points		= map(lambda p: mm_to_px(*p),[(0,0),(700,0),(700,25),(0,25)])
		)
		self.lance = 0
		self.filet = 0

	def __repr__(self):
		return "Mammouth %s " % (self.posinit,)
