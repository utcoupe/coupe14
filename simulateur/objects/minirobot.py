# -*- coding: utf-8 -*-

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))
sys.path.append(os.path.join(DIR_PATH, "..", "objects"))

from define import *
from engine.engineobject import EngineObjectPoly
from objects import robot


class MiniRobot(robot.Robot):
	"""
	Classe fille de la classe robot.
	Regroupe les méthodes en lien avec les actions que seul le gros robot peut exécuter.
	"""

	#définition des données graphiques et physiques
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

		self.bras_gauche = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_BRAS_PETIT,
			offset		= mm_to_px(HEIGHT_MINI/2-10,-WIDTH_MINI+35),
			color		= "purple",
			poly_points = map(lambda p: mm_to_px(*p),[(0,0),(10,0),(10,70), (0,70)]), #taille du bras
			is_extension= True
		)

		self.bras_droite = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_BRAS_PETIT,
			offset		= mm_to_px(HEIGHT_MINI/2-10,WIDTH_MINI/2),
			color		= "purple",
			poly_points = map(lambda p: mm_to_px(*p),[(0,0),(10,0),(10,70), (0,70)]), #taille du bras
			is_extension= True
		)

		robot.Robot.__init__(self,
			engine 				= engine,
			team				= team,
			posinit				= posinit,
			mass				= 10,
			typerobot			= MINI,
			colltype 			= COLLTYPE_PETIT_ROBOT,
			poly_points			= mm_to_px((0,0),(HEIGHT_MINI,0),(HEIGHT_MINI,WIDTH_MINI),(0,WIDTH_MINI)),
		)

		self.add_body_extension(self.avant)
		self.__bras_used = None #pour savoir quel bras est sorti
		self.__nbr_lances = 6
		self.__filet = 1
		self.__fresques = 2
		self.setRobotType(MINI)

	def getNbrLances(self):
		return self.__nbr_lances

	def getFilet(self):
		return self.__filet

	def getNbrFresques(self):
		return self.__fresques

	def lancerBalle(self, nbr):
		if self.__nbr_lances - nbr >= 0:
			self.__nbr_lances -= nbr

	def accrocherFresques(self):
		if self.__fresques > 0:
			self.__fresques -= 1

	def tirFilet(self):
		if self.__filet > 0:
			self.__filet = 0

	def ouvrirBras(self, position):
		"""
		Actionne le bras du robot du côté voulu par le paramètre position.
		Le côté du bras dépend aussi de l'orientation du robot.
		Si un bras différent de celui qui est sorti est appelé, c'est le bras appelé qui sera affiché.
		@param position int (0 = suppresion du robot; 1 = bras gauche; -1 = bras droit)
		"""
		if position == 0:
			if self.__bras_used is not None:
				self.remove_body_extension(self.__bras_used)
				self.__bras_used = None
		elif position == -1:
			if self.__bras_used is None:
				self.add_body_extension(self.bras_gauche)
				self.__bras_used = self.bras_gauche
			elif self.__bras_used == self.bras_droite:
				self.remove_body_extension(self.__bras_used)
				self.add_body_extension(self.bras_gauche)
				self.__bras_used = self.bras_gauche
		elif position == 1:
			if self.__bras_used is None:
				self.add_body_extension(self.bras_droite)
				self.__bras_used = self.bras_droite
			elif self.__bras_used == self.bras_gauche:
				self.remove_body_extension(self.__bras_used)
				self.add_body_extension(self.bras_droite)
				self.__bras_used = self.bras_droite
		else:
			print('minibot.ouvrirBras mauvaise position du bras')