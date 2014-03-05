# -*- coding: utf-8 -*-
"""
Classe pour toutes les autres données
"""

from constantes import *
import time

class MetaData():
	def __init__(self):
		self.__number_of_enemy = NUMBER_OF_ENEMY
		self.__seuil_rouge = SEUIL_ROUGE
		self.__seuil_jaune = SEUIL_JAUNE

		#Variables
		self.__triangle_en_position = ("Rien", 0) #(Rien ou JAUNE ou ROUGE, timestanp de l'info pour savoir si on peut l'utiliser directment ou non)
		self.__in_game = False
		self.__in_funny_action = False
		self.__game_clock = None


	#utilise les données en provenance des caméras pour mettre à jour les données de la classe
	def majCam(self, arguments):
		if arguments[0] > self.__seuil_rouge and arguments[1] > self.__seuil_jaune:
			print("Probleme, les deux seuils sont dépassés")
		elif arguments[0] > self.__seuil_rouge:
			self.__triangle_en_position = ("Rouge", int(time.time()*1000))
		elif arguments[1] > self.__seuil_jaune:
			self.__triangle_en_position = ("Jaune", int(time.time()*1000))
		else:
			self.__triangle_en_position = ("Rien", int(time.time()*1000))

	def startMatch(self):
		if self.__in_game == False:
			self.__in_game = True
			self.__game_clock = 0
		else:
			print("WARNING: Demande de debut de match alors que le match est déjà en cours.")

	def stopMatch(self):
		if self.__in_game == True:
			self.__in_game = False
		else:
			print("WARNING: Demande de fin de match alors que le match est déjà en arreté.")
	
	def startFunny(self):
		if self.__in_funny_action == False:
			self.__in_funny_action = True
		else:
			print("WARNING: Demande de debut funny action alors que funny action est déjà en cours.")

	def stopFunny(self):
		if self.__in_funny_action == True:
			self.__in_funny_action = False
		else:
			print("WARNING: Demande la fin de funny action alors que funny action est arreté.")

	def getInGame(self):
		return self.__in_game

	def setGameClock(self, clock):
		print(self.__game_clock, self.__in_game, self.__in_funny_action)
		self.__game_clock = clock