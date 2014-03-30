# -*- coding: utf-8 -*-


import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectSegment


class Wall(EngineObjectSegment):
	def __init__(self, engine, posa, posb):
		EngineObjectSegment.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_WALL,
			posA			= posa,
			posB			= posb,
			color			= "black",
			mass			= MASS_INF,
			width			= 2
		)

	def __repr__(self):
		return "Wall"
	
