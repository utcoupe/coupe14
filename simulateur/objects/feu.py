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
		self.__extension_down = None #variable qui stock l'extension utilisée pour coucher le feu
		self.__eteindre_flag = False

	def getPositionPixel(self):
		"""
		@return position du feu en pixel
		"""
		return self.body.position[0],self.body.position[1]

	def eteindre(self):
		"""
		Supprime de la map le feu concerné
		"""
		if self.__eteindre_flag == False:
			self.removeExtension()
			self.engine.objects_to_remove.append(self)
			self.__eteindre_flag = True

	def removeExtension(self):
		"""
		Permet de supprimer l'extension du feu quand il est couché
		"""
		if self.__extension_down is not None:
			self.remove_body_extension(self.__extension_down)
			self.__is_down = False
			self.__extension_down = None

	def coucher(self, position_robot, type_bras):
		"""
		Permet de coucher le feu sur la map (quand le bras du robot le percute)
		@param position_robot = 'g' ou 'd' (gauche/droite)
		@param type_bras = 'open' ou 'close'
		"""
		if self.__extension_down is not None:
			return
		if(position_robot == 'g'):
			if(type_bras == 'open'): #coucher le feu à droite
				if(self.__coucher_a_droite == 'r'):
					self.__addCoucherExtension(self.triangleRedDroite)
				else:
					self.__addCoucherExtension(self.triangleYellowDroite)
			else: #coucher le feu à gauche
				if(self.__coucher_a_gauche == 'r'):
					self.__addCoucherExtension(self.triangleRedGauche)
				else:
					self.__addCoucherExtension(self.triangleYellowGauche)
		else:
			if(type_bras == 'open'): #coucher le feu à gauche
				if(self.__coucher_a_gauche == 'r'):
					self.__addCoucherExtension(self.triangleRedGauche)
				else:
					self.__addCoucherExtension(self.triangleYellowGauche)
			else: #coucher le feu à droite
				if(self.__coucher_a_droite == 'r'):
					self.__addCoucherExtension(self.triangleRedDroite)
				else:
					self.__addCoucherExtension(self.triangleYellowDroite)
		self.__is_down = True
		self.__eteindre_flag = False

	def __addCoucherExtension(self, extension):
		if self.__extension_down is None:
			self.add_body_extension(extension)
			self.__extension_down = extension

	def coucherFeuCouleur(self, color):
		"""
		Color le feu suivant la couleur
		@param color couleur du feu
		"""
		if color == RED:
			self.__addCoucherExtension(self.triangleRedDroite)
		else:
			self.__addCoucherExtension(self.triangleYellowDroite)

	def getOrientation(self):
		"""
		@return orientation du feu
		"""
		return self.orientation

	def __repr__(self):
		return "Feu %s " % (self.posinit,)

