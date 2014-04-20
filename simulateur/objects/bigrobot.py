# -*- coding: utf-8 -*-

from .robot import Robot
import math
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectPoly

class BigRobot(Robot):
	def __init__(self, *, engine, posinit, team):
		self.bras = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_BRAS,
			offset		= mm_to_px(WIDTH_GROS/2-25, HEIGHT_GROS/2+25),
			color		= "purple",
			poly_points = map(lambda p: mm_to_px(*p),[(0,0),(LONGUEUR_BRAS,0),(0,-LONGUEUR_BRAS)]), #taille du bras
			is_extension= True
		)

		Robot.__init__(self,
			engine		 		= engine,
			team				= team,
			posinit				= posinit,
			mass				= 10,
			typerobot			= BIG,
			colltype 			= COLLTYPE_GROS_ROBOT,
			poly_points			= mm_to_px((0,0),(HEIGHT_GROS,0),(HEIGHT_GROS,WIDTH_GROS),(0,WIDTH_GROS)),
			extension_objects	= [],
		)
		self.__state_jack = 0  # jack in
		self.body.angle = math.radians(90)
		self.add_bras()

	def add_bras(self):
		self.add_body_extension(self.bras)

	def getStateJack(self):
		return self.__state_jack
