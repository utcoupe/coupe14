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
		self.__bras_used = None #pour savoir quel bras est sorti
		self.__nbr_lances = 6
		self.__filet = 1
		self.__fresques = 2
		self.__state_jack = 1  # jack in

	def getStateJack(self):
		return self.__state_jack

	def setStateJack(self):
		self.__state_jack = 0

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

