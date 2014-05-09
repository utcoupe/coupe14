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
		MetaData.setFirstPositionFlussmittel([200, 1850, -1.55]) #TODO, à parametrer en fonction de la couleur de debut
		MetaData.setFirstPositionTibot([193, 1542, -0.42203])#TODO
	elif color == "YELLOW":
		MetaData.setFirstPositionFlussmittel([2800, 1850, -1.55]) #TODO, utiliser des constantes
		MetaData.setFirstPositionTibot([2807, 1542, -2.71797])#TODO
	else:
		logger.error("Aucun couleur n'a été défini, notre couleur: " + str(color))