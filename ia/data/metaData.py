# -*- coding: utf-8 -*-
"""
Classe pour toutes les autres données
"""

import time

class MetaData():
	def __init__(self, constantes):
		self.numberOfenemy = constantes.number_of_enemy
		self.seuilRouge = constantes.seuil_rouge
		self.seuilJaune = constantes.seuil_jaune

		#Variables
		self.triangleEnPosition = ("Rien", 0) #(Rien ou JAUNE ou ROUGE, timestanp de l'info pour savoir si on peut l'utiliser directment ou non)


	#utilise les données en provenance des caméras pour mettre à jour les données de la classe
	def majCam(self, arguments):
		if arguments[0] > seuilRouge and arguments[1] > seuilJaune:
			print("Probleme, les deux seuils sont dépassés")
		elif arguments[0] > seuilRouge:
			self.triangleEnPosition = ("Rouge", int(time.time()*1000))
		elif arguments[1] > seuilJaune:
			self.triangleEnPosition = ("Jaune", int(time.time()*1000))
		else:
			self.triangleEnPosition = ("Rien", int(time.time()*1000))
