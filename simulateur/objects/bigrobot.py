# -*- coding: utf-8 -*-

from .robot import Robot
import math
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *

class BigRobot(Robot):
	def __init__(self, *, engine, posinit, team):
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

	def getStateJack(self):
		return self.__state_jack
