# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys
import time

#Nos fichiers
from communication import communicationGlobale
from data import data
import constantes
import guiCommande

Constantes = constantes.Constantes()
ObjetCommunication = communicationGlobale.CommunicationGlobale(Constantes)
arduino_constantes = ObjetCommunication.getConst()

data = data.Data(ObjetCommunication, Constantes, arduino_constantes)

try:
	while True:
		time.sleep(1000/1000.0)
except KeyboardInterrupt:
	#objetCommunication.stopGestion()
	pass
finally:
	#objetCommunication.stopGestion()
	pass
