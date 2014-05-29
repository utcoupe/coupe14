# -*- coding: utf-8 -*-
"""
Ce fichier regroupe les systèmes à configurer avant le debut d'un match
"""
import logging
from constantes import *

logger = logging.getLogger(__name__.split('.')[0])

def parametrerHokuyo():
	#TODO
	pass

def parametrerIa(MetaData, color):
	MetaData.setOurColor(color)


	if color == "RED":
		MetaData.setFirstPositionFlussmittel(START_POSITION_RED_FLUSSMITTEL)
		MetaData.setFirstPositionTibot(START_POSITION_RED_TIBOT)
	elif color == "YELLOW":
		MetaData.setFirstPositionFlussmittel((3000 - START_POSITION_RED_FLUSSMITTEL[0], START_POSITION_RED_FLUSSMITTEL[1], -3.1415 - START_POSITION_RED_FLUSSMITTEL[2]))
		MetaData.setFirstPositionTibot((3000 - START_POSITION_RED_TIBOT[0], START_POSITION_RED_TIBOT[1], -3.1415 - START_POSITION_RED_TIBOT[2]))
	else:
		logger.error("Aucun couleur n'a été défini, notre couleur: " + str(color))