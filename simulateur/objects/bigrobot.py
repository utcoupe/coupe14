# -*- coding: utf-8 -*-

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
from objects import robot
import time

class BigRobot(robot.Robot):
	"""
	Classe fille de la classe robot.
	Regroupe les méthodes en lien avec les actions que seul le gros robot peut exécuter.
	"""

	#définition des données graphiques et physiques
	def __init__(self, *, engine, posinit, team):
		self.bras = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_BRAS,
			offset		= mm_to_px(WIDTH_GROS/2-21, -HEIGHT_GROS/2-24),
			color		= "green",
			poly_points = map(lambda p: mm_to_px(*p),[(LONGUEUR_BRAS,0),(0,LONGUEUR_BRAS), (0,0)]), #taille du bras
			is_extension= True
		)

		self.bras_ouvrir = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_BRAS_OUVRIR,
			offset		= mm_to_px(WIDTH_GROS/2-21, -HEIGHT_GROS/2-24),
			color		= "purple",
			poly_points = map(lambda p: mm_to_px(*p),[(LONGUEUR_BRAS,0),(0,LONGUEUR_BRAS), (0,0)]), #taille du bras
			is_extension= True
		)

		self.bras_fermer = EngineObjectPoly(
			engine 		= engine,
			colltype	= COLLTYPE_BRAS_FERMER,
			offset		= mm_to_px(WIDTH_GROS/2-21, -HEIGHT_GROS/2-24),
			color		= "blue",
			poly_points = map(lambda p: mm_to_px(*p),[(LONGUEUR_BRAS,0),(0,LONGUEUR_BRAS), (0,0)]), #taille du bras
			is_extension= True
		)

		robot.Robot.__init__(self,
			engine		 		= engine,
			team				= team,
			posinit				= posinit,
			mass				= 10,
			typerobot			= BIG,
			colltype 			= COLLTYPE_GROS_ROBOT,
			poly_points			= mm_to_px((0,0),(HEIGHT_GROS,0),(HEIGHT_GROS,WIDTH_GROS-95),(HEIGHT_GROS-115,WIDTH_GROS),(0,WIDTH_GROS)),
			extension_objects	= [],
		)
		self.__nbrFeuAvant = 0
		self.__nbrFeuArriere = 0
		self.__engine = engine
		self.__feuHit = 0
		self.__feuHit_forced = False
		self.setRobotType(BIG)

	def getFeuxAvant(self):
		return self.__nbrFeuAvant

	def getFeuxArriere(self):
		return self.__nbrFeuArriere

	def setFeuHit(self, value):
		if self.__feuHit_forced == False:
			self.__feuHit = value
		elif self.__feuHit_forced == True:
			self.__feuHit = 0

	def getFeuHit(self):
		"""
		feuHit fonctionne comme un flag, une fois qu'il est lu sa valeur revient par défaut
		"""
		return self.__feuHit

	def forceFailFeuHit(self, value):
		self.__feuHit_forced = value

	def activerVisio(self):
		"""
		Active la reconnaissance de triangles dans la zone de portée du bras.
		Concrètement on crée l'extension bras pendant un laps de temps très court.
		"""
		save_pos = self.getPosition()
		self.add_body_extension(self.bras)
		time.sleep(0.5) #temps où le bras apparaitra
		self.remove_body_extension(self.bras)
		self.setPosition(save_pos[0],save_pos[1],save_pos[2])

	def activerBrasOuvrir(self):
		"""
		Simule le bras qui sort avec un BRAS_OUVRIR
		"""
		save_pos = self.getPosition()
		self.add_body_extension(self.bras_ouvrir)
		time.sleep(0.1) #temps où le bras apparaitra
		self.remove_body_extension(self.bras_ouvrir)
		self.setPosition(save_pos[0],save_pos[1],save_pos[2])

	def activerBrasFermer(self):
		"""
		Simule le bras qui rentre avec un BRAS_FERMER
		"""
		save_pos = self.getPosition()
		self.add_body_extension(self.bras_fermer)
		time.sleep(0.1) #temps où le bras apparaitra
		self.remove_body_extension(self.bras_fermer)
		self.setPosition(save_pos[0],save_pos[1],save_pos[2])

	def storeFeu(self, sens):
		"""
		Stock un feu dans le robot
		@param sens int détermine si on stocke le feu à l'avant ou à l'arrière du robot
		"""
		if sens > 0:
			self.__nbrFeuAvant += 1
		else:
			self.__nbrFeuArriere += 1

	def dropFeu(self,x,y):
		"""
		Va déposer un feu à l'avant du robot
		@param x,y : endroit où déposer le feu
		"""
		if self.__nbrFeuAvant > 0:
			self.__nbrFeuAvant -= 1
			new_feu = feu.Feu(self.__engine,(self.__computePositionTriangleAvant(x,y)),"vert",True)
			self.__engine.add(new_feu)
			new_feu.coucherFeuCouleur(self.getTeam()) #pour donner la bonne couleur au feu
		else:
			print('pas de feu stocké à avant du robot')

	def releaseFeuArriere(self):
		"""
		Ejecte un feu à l'arrière du robot
		"""
		#print('release feu arriere, NBR : ', self.__nbrFeuArriere)
		if (self.__nbrFeuArriere > 0):
			self.__nbrFeuArriere -= 1
			new_feu = feu.Feu(self.__engine,(self.__computePositionTriangleArriere()),"vert",True)
			self.__engine.add(new_feu)
			new_feu.coucherFeuCouleur(self.getTeam()) #pour donner la bonne couleur au feu
		else:
			print('pas de feu stocké à arriere du robot')

	def __computePositionTriangleArriere(self):
		"""
		Calcule la position où éjecter le triangle derrière le robot
		"""
		xBot = self.body.position[0]
		yBot = self.body.position[1]
		aBot = self.body.angle
		dist_feu_robot = 40+55+15 #40 = distance/extrémité, 55 = taille triangle feu, 15 = distance milieu/extrémité feu
		xFeu = (int)(xBot - math.ceil(mm_to_px(dist_feu_robot + WIDTH_GROS/2)*math.cos(aBot)))
		yFeu = (int)(yBot - math.ceil(mm_to_px(dist_feu_robot + WIDTH_GROS/2)*math.sin(aBot)))
		return xFeu,yFeu

	def __computePositionTriangleAvant(self,xFeu,yFeu):
		"""
		Calcule la position où éjecter le triangle devant le robot
		"""
		xBot = mm_to_px(self.getXreal())
		yBot = mm_to_px(2000 - self.getYreal())
		aBot = self.body.angle
		dist_feu_robot = mm_to_px(math.sqrt(xFeu*xFeu + yFeu*yFeu))
		xPosFeu = (int)(xBot + math.ceil(dist_feu_robot*math.cos(aBot)))
		yPosFeu = (int)(yBot + math.ceil(dist_feu_robot*math.sin(aBot)))
		#print("__computePositionTriangleAvant : ",px_to_mm(xPosFeu),2000-px_to_mm(yPosFeu),self.body.angle)
		return xPosFeu,yPosFeu