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

<<<<<<< HEAD
com = communicationGlobale.communicationGlobale("/dev/ttyUSB0", 57600, "ODD", "/dev/ttymxc3", 115200, "NONE")
=======
constantes = constantes.constantes()
objetCommunication = communicationGlobale.communicationGlobale(constantes)
arduinoConstantes = objetCommunication.getConst()
>>>>>>> 5ee141fd0a5e07cbd4452a6c611eb39cb8da2cca

data = globaleData.Data(objetCommunication, constantes, arduinoConstantes)

try:
	while True:
		pass
except KeyboardInterrupt:
	#objetCommunication.stopGestion()
	pass
finally:
	#objetCommunication.stopGestion()
	pass
