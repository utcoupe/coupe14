# -*- coding: utf-8 -*-

from .robot import Robot
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectPoly


class MiniRobot(Robot):
	def __init__(self, *, engine, posinit, team):
		#extension pour donner un signe distinctif au robot pour reconnaitre l'avant
		self.avant = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_PETIT_ROBOT,
			offset		= mm_to_px(HEIGHT_MINI/2,-WIDTH_MINI/2),
			color		= "black",
			poly_points = map(lambda p: mm_to_px(*p),[(0,0),(0,WIDTH_MINI),(-10,WIDTH_MINI),(-10,0)]), #taille du bras
			is_extension= True
		)

		Robot.__init__(self,
			engine 				= engine,
			team				= team,
			posinit				= posinit,
			mass				= 10,
			typerobot			= MINI,
			colltype 			= COLLTYPE_PETIT_ROBOT,
			poly_points			= mm_to_px((0,0),(HEIGHT_MINI,0),(HEIGHT_MINI,WIDTH_MINI),(0,WIDTH_MINI)),
		)

		self.add_body_extension(self.avant)