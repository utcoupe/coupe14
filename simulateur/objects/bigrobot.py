# -*- coding: utf-8 -*-

from .robot import Robot
import math
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))
sys.path.append(os.path.join(DIR_PATH, "..", "objects"))

from define import *
from engine.engineobject import EngineObjectPoly
from objects import feu

class BigRobot(Robot):
	def __init__(self, *, engine, posinit, team):
		self.bras = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_BRAS,
			offset		= mm_to_px(WIDTH_GROS/2-21, -HEIGHT_GROS/2-24),
			color		= "green",
			poly_points = map(lambda p: mm_to_px(*p),[(LONGUEUR_BRAS,0),(0,LONGUEUR_BRAS), (0,0)]), #taille du bras
			is_extension= True
		)

		Robot.__init__(self,
			engine		 		= engine,
			team				= team,
			posinit				= posinit,
			mass				= 10,
			typerobot			= BIG,
			colltype 			= COLLTYPE_GROS_ROBOT,
			poly_points			= mm_to_px((0,0),(HEIGHT_GROS,0),(HEIGHT_GROS,WIDTH_GROS-95),(HEIGHT_GROS-115,WIDTH_GROS),(0,WIDTH_GROS)),
			extension_objects	= [],
		)
		self.__state_jack = 0  # jack in
		self.__nbrFeu = 0
		self.__engine = engine

	def add_bras(self):
		self.add_body_extension(self.bras)

	def remove_bras(self):
		self.remove_body_extension(self.bras)

	def storeFeu(self):
		self.__nbrFeu += 1

	def releaseFeu(self):
		if (self.__nbrFeu > 0):
			self.__nbrFeu -= 1
			self.__engine.add(feu.Feu(self.__engine,mm_to_px(int(1500),int(1000)),"vert",True))
		else:
			print('fuck, j''ai pas de feu !')

	def getStateJack(self):
		return self.__state_jack
