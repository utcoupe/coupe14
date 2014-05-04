# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectCircle, EngineObjectPoly



class FoyerCentre(EngineObjectCircle):
	def __init__(self,engine,posinit):
		EngineObjectCircle.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_FOYER,
			posinit			= posinit,
			color			= "brown",
			mass 			= MASS_INF,
			radius			= mm_to_px(150),
			layers			= 1
		)
		self.__nbFeu = 0

	def __repr__(self):
		return "FoyerCentre %s " % (self.posinit,)

class FoyerBord(EngineObjectPoly):
	def __init__(self,engine,posinit,position):
		if (position == "droite"):
			points = map(lambda p: mm_to_px(*p),[(0,0),(-250,-0),(-241,-65),(-217,-125),(-177,-177),(-125,-217),(-65,-241),(-0,-250)])
		elif(position == "gauche"):
			points = map(lambda p: mm_to_px(*p),[(0,0),(250,0),(241,-65),(217,-125),(177,-177),(125,-217),(65,-241),(0,-250)])
		EngineObjectPoly.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_FOYER,
			posinit			= posinit,
			color			= "brown",
			mass 			= MASS_INF,
			poly_points		= points
		)
		self.__nbFeu = 0

	def __repr__(self):
		return "FoyerBord %s " % (self.posinit,)
