# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectPoly



class Arbre(EngineObjectPoly):
	def __init__(self,engine,posinit, orientation):
		if (orientation == "droite"):
			points = map(lambda p: mm_to_px(*p),[(0,0),(75,20),(130,75),(150,150),(130,225),(75,280),(0,300)])
		elif(orientation == "gauche"):
			points = map(lambda p: mm_to_px(*p),[(0,300),(-75,280),(-130,225),(-150,150),(-130,75),(-75,20),(0,0)])
		else:
			points = map(lambda p: mm_to_px(*p),[(0,0),(20,-75),(75,-130),(150,-150),(225,-130),(280,-75),(300,0)])
		EngineObjectPoly.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_ARBRE,
			posinit			= posinit,
			color			= "green",
			mass 			= MASS_INF,
			poly_points		= points
		)
	
	def __repr__(self):
		return "Arbre %s " % (self.posinit,)
