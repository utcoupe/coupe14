__author__ = 'furmi'

# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectPoly

class Feu(EngineObjectPoly):
	def __init__(self,engine,posinit, orientation):
		if (orientation == "vert"): # |
			points_feu = map(lambda p: mm_to_px(*p),[(0,0),(30,0),(30,140),(0,140)])
			points_triangle = map(lambda p: mm_to_px(*p),[(0,0),(70,55),(0,140)])
			offset_triangle = mm_to_px(15,-70)
		else: # ---
			points_feu = map(lambda p: mm_to_px(*p),[(0,0),(140,0),(140,30),(0,30)])
			points_triangle = map(lambda p: mm_to_px(*p),[(0,0),(55,70),(140,0)])
			offset_triangle = mm_to_px(-70,15)
		EngineObjectPoly.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_FEU,
			posinit			= posinit,
			mass			= 80,
			poly_points		= points_feu
		)

		self.triangle = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_FEU,
			offset		= offset_triangle,
			color		= "purple",
			poly_points = points_triangle,
			is_extension= True
		)
		self.__is_down = False
		#self.coucher_feu()

	def eteindre(self):
		"""
		Supprime de la map le feu concerné
		"""
		self.engine.objects_to_remove.append(self)

	def coucher_feu(self):
		self.add_body_extension(self.triangle)
		self.__is_down = True

	def lever_feu(self):
		self.remove_body_extension(self.triangle)
		self.__is_down = False

	def __repr__(self):
		return "Feu %s " % (self.posinit,)

