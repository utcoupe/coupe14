# -*- coding: utf-8 -*-
"""
Classe pour toutes les autres données
"""

from constantes import *
import time
import logging

class MetaData():
	def __init__(self):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.numberOfenemy = NUMBER_OF_ENEMY

		#Constantes à initialiser 
		self.__first_position_flussmittel = None #position est un tableau [x, y, angle]
		self.__first_position_tibot = None
		self.__our_color = None

		#Variables
		self.__triangle_en_position = ("Rien", 0) #(Rien ou JAUNE ou ROUGE, timestanp de l'info pour savoir si on peut l'utiliser directment ou non)
		self.__in_game = False
		self.__in_funny_action = False
		self.__checkCollision = False #Demarrage différé des collisions pour eviter le cas particulier du debut de match 
		self.__game_clock = None
		self.__collision_threshold = COLLISION_THRESHOLD


	def getFirstPositionFlussmittel(self):
		return self.__first_position_flussmittel

	def setFirstPositionFlussmittel(self, position):
		"""position est un tableau [x, y, angle]"""
		self.__first_position_flussmittel = position

	def getFirstPositionTibot(self):
		return self.__first_position_tibot

	def setFirstPositionTibot(self, position):
		"""position est un tableau [x, y, angle]"""
		self.__first_position_tibot = position

	def getOurColor(self):
		return self.__our_color

	def getCollisionThreshold(self):
		return self.__collision_threshold

	def setOurColor(self, color):
		"""prend en parametre "RED" ou "YELLOW" """
		self.__our_color = color

	def setCollisionThreshold(threshold):
		self.__collision_threshold = threshold

		
	#utilise les données en provenance des caméras pour mettre à jour les données de la classe
	def majCam(self, arguments):
		if arguments[0] > SEUIL_ROUGE and arguments[1] > SEUIL_JAUNE:
			self.__logger.warning("Probleme, les deux seuils sont dépassés")
		elif arguments[0] > SEUIL_ROUGE:
			self.__triangle_en_position = ("Rouge", int(time.time()*1000))
		elif arguments[1] > SEUIL_JAUNE:
			self.__triangle_en_position = ("Jaune", int(time.time()*1000))
		else:
			self.__triangle_en_position = ("Rien", int(time.time()*1000))

	def startMatch(self):
		if self.__in_game == False:
			self.__in_game = True
			self.__game_clock = 0
		else:
			self.__logger.warning("Demande de debut de match alors que le match est déjà en cours.")

	def stopMatch(self):
		if self.__in_game == True:
			self.__in_game = False
		else:
			self.__logger.warning("Demande de fin de match alors que le match est déjà en arreté.")
	
	def startFunny(self):
		if self.__in_funny_action == False:
			self.__in_funny_action = True
		else:
			self.__logger.error("Demande de debut funny action alors que funny action est déjà en cours.")

	def stopFunny(self):
		if self.__in_funny_action == True:
			self.__in_funny_action = False
		else:
			self.__logger.error("Demande la fin de funny action alors que funny action est arreté.")

	def startCheckCollision(self):
		self.__logger.info("On commencer à verifier les collisions")
		self.__checkCollision = True

			# GETTER
	def getInGame(self):
		return self.__in_game

	def getInFunnyAction(self):
		return self.__in_funny_action

	def getGameClock(self):
		return self.__game_clock

	def getCheckCollision(self):
		return self.__checkCollision

			#SETTER
	def setGameClock(self, clock):
		self.__game_clock = clock
