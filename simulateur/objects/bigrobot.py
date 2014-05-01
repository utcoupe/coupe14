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
		self.__nbrFeuAvant = 0
		self.__nbrFeuArriere = 0 #normalement à 0, 1 pour les tests
		self.__engine = engine
		self.__feuHit = 0

	def setFeuHit(self, value):
		self.__feuHit = value

	def getFeuHit(self):
		"""
		feuHit fonctionne comme un flag, une fois qu'il est lu sa valeur revient par défaut
		"""
		return self.__feuHit

	def activerVisio(self):
		"""
		Active la reconnaissance de triangles dans la zone de portée du bras
		"""
		self._visio.actionBras()

	def add_bras(self):
		self.add_body_extension(self.bras)

	def remove_bras(self):
		self.remove_body_extension(self.bras)

	def storeFeu(self, sens):
		if sens > 0:
			self.__nbrFeuAvant += 1
		else:
			self.__nbrFeuArriere += 1

	def releaseFeuArriere(self):
		print('release feu arriere, NBR : ', self.__nbrFeuArriere)
		if (self.__nbrFeuArriere > 0):
			self.__nbrFeuArriere -= 1
			self.__engine.add(feu.Feu(self.__engine,(self.__computePositionTriangle()),"vert",True))
		else:
			print('pas de feu stocké à arriere du robot')

	def getStateJack(self):
		return self.__state_jack

	def __computePositionTriangle(self):
		xBot = self.body.position[0]
		yBot = self.body.position[1]
		aBot = self.body.angle
		dist_feu_robot = 40+55+15 #40 = distance/extrémité, 55 = taille triangle feu, 15 = distance milieu/extrémité feu
		xFeu = (int)(xBot - math.ceil(mm_to_px(dist_feu_robot + WIDTH_GROS/2)*math.cos(aBot)))
		yFeu = (int)(yBot - math.ceil(mm_to_px(dist_feu_robot + WIDTH_GROS/2)*math.sin(aBot)))
		return xFeu,yFeu