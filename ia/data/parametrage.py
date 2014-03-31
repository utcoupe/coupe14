# -*- coding: utf-8 -*-
"""
Ce fichier regroupe les systèmes à configurer avant le debut d'un match
"""
import logging

logger = logging.getLogger(__name__.split('.')[0])

def parametrerHokuyo():
	#TODO
	pass

def parametrerIa(MetaData, color):
	MetaData.setOurColor(color)

	if color == "RED":
		MetaData.setFirstPositionFlussmittel([50, 1950, -3.15/2]) #TODO, à parametré en fonction de la couleur de debut
		MetaData.setFirstPositionTibot([50, 1700, 0.0])#TODO
	elif color == "YELLOW":
		MetaData.setFirstPositionFlussmittel([50, 1950, -3.15/2]) #TODO, utilmiser des constantes
		MetaData.setFirstPositionTibot([50, 1700, 0.0])#TODO
	else:
		logger.error("Aucun couleur n'a été défini, notre couleur: " + str(color))