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
		self.seuilRouge = SEUIL_ROUGE
		self.seuilJaune = SEUIL_JAUNE

		#Variables
		self.triangleEnPosition = ("Rien", 0) #(Rien ou JAUNE ou ROUGE, timestanp de l'info pour savoir si on peut l'utiliser directment ou non)


	#utilise les données en provenance des caméras pour mettre à jour les données de la classe
	def majCam(self, arguments):
		if arguments[0] > seuilRouge and arguments[1] > seuilJaune:
			self.__logger.warning("Probleme, les deux seuils sont dépassés")
		elif arguments[0] > seuilRouge:
			self.triangleEnPosition = ("Rouge", int(time.time()*1000))
		elif arguments[1] > seuilJaune:
			self.triangleEnPosition = ("Jaune", int(time.time()*1000))
		else:
			self.triangleEnPosition = ("Rien", int(time.time()*1000))
