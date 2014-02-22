# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys

#Nos fichiers
from communication import communicationGlobale
from data import globaleData
import constantes
import guiCommande

constantes = constantes.constantes()
objetCommunication = communicationGlobale.communicationGlobale(constantes)
arduinoConstantes = objetCommunication.getConst()

#data = globaleData.Data(objetCommunication, constantes, arduinoConstantes)

try:
	while True:
		pass
except KeyboardInterrupt:
	#objetCommunication.stopGestion()
	pass
finally:
	#objetCommunication.stopGestion()
	pass
