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
	def __init__(self,engine,posinit, orientation, sens, coucher = False):
		if (orientation == "vert"): # |
			points_feu = map(lambda p: mm_to_px(*p),[(0,0),(30,0),(30,140),(0,140)])
			points_triangle_rd = map(lambda p: mm_to_px(*p),[(0,0),(70,55),(0,140)])
			offset_triangle_rd = mm_to_px(15,-70)
			points_triangle_yg = map(lambda p: mm_to_px(*p),[(0,0),(70,55),(0,140)])
			offset_triangle_yg = mm_to_px(15,-70)
			points_triangle_rg = map(lambda p: mm_to_px(*p),[(0,0),(-70,55),(0,140)])
			offset_triangle_rg = mm_to_px(-15,-70)
			points_triangle_yd = map(lambda p: mm_to_px(*p),[(0,0),(-70,55),(0,140)])
			offset_triangle_yd = mm_to_px(-15,-70)
		else: # ---
			points_feu = map(lambda p: mm_to_px(*p),[(0,0),(140,0),(140,30),(0,30)])
			points_triangle_rd = map(lambda p: mm_to_px(*p),[(0,0),(55,70),(140,0)])
			offset_triangle_rd = mm_to_px(-70,15)
			points_triangle_yg = map(lambda p: mm_to_px(*p),[(0,0),(55,70),(140,0)])
			offset_triangle_yg = mm_to_px(-70,15)
			points_triangle_rg = map(lambda p: mm_to_px(*p),[(0,0),(55,-70),(140,0)])
			offset_triangle_rg = mm_to_px(-70,-15)
			points_triangle_yd = map(lambda p: mm_to_px(*p),[(0,0),(55,-70),(140,0)])
			offset_triangle_yd = mm_to_px(-70,-15)

		EngineObjectPoly.__init__(self,
			engine			= engine,
			colltype		= COLLTYPE_FEU,
			posinit			= posinit,
			mass			= 80,
			poly_points		= points_feu,
			layers			= 2
		)

		self.triangleRedDroite = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_FEU,
			offset		= offset_triangle_rd,
			color		= "red",
			poly_points = points_triangle_rd,
			layers			= 2,
			is_extension= True
		)

		self.triangleYellowGauche = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_FEU,
			offset		= offset_triangle_yd,
			color		= "yellow",
			poly_points = points_triangle_yd,
			layers			= 2,
			is_extension= True
		)

		self.triangleRedGauche= EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_FEU,
			offset		= offset_triangle_rg,
			color		= "red",
			poly_points = points_triangle_rg,
			layers			= 2,
			is_extension= True
		)

		self.triangleYellowDroite = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_FEU,
			offset		= offset_triangle_yg,
			color		= "yellow",
			poly_points = points_triangle_yg,
			layers			= 2,
			is_extension= True
		)

		self.orientation = orientation
		if (sens == 'r'):
			self.__coucher_a_gauche = 'y'
			self.__coucher_a_droite = 'r'
		else:
			self.__coucher_a_gauche = 'r'
			self.__coucher_a_droite = 'y'
		self.__is_down = False

	def getPositionPixel(self):
		return self.body.position[0],self.body.position[1]

	def eteindre(self):
		"""
		Supprime de la map le feu concerné
		"""
		self.engine.objects_to_remove.append(self)

	def coucher(self, position_robot, type_bras):
		"""
		Permet de coucher le feu sur la map
		@param position_robot = 'g' ou 'd' (gauche/droite)
		@param type_bras = 'open' ou 'close'
		"""
		if(position_robot == 'g'):
			if(type_bras == 'open'): #coucher le feu à droite
				if(self.__coucher_a_droite == 'r'):
					self.add_body_extension(self.triangleRedDroite)
				else:
					self.add_body_extension(self.triangleYellowDroite)
			else: #coucher le feu à gauche
				if(self.__coucher_a_gauche == 'r'):
					self.add_body_extension(self.triangleRedGauche)
				else:
					self.add_body_extension(self.triangleYellowGauche)
		else:
			if(type_bras == 'open'): #coucher le feu à gauche
				if(self.__coucher_a_gauche == 'r'):
					self.add_body_extension(self.triangleRedGauche)
				else:
					self.add_body_extension(self.triangleYellowGauche)
			else: #coucher le feu à droite
				if(self.__coucher_a_droite == 'r'):
					self.add_body_extension(self.triangleRedDroite)
				else:
					self.add_body_extension(self.triangleYellowDroite)
		self.__is_down = True

	def lever_feu(self):
		self.remove_body_extension(self.triangle)
		self.__is_down = False

	def getOrientation(self):
		return self.orientation

	def __repr__(self):
		return "Feu %s " % (self.posinit,)

