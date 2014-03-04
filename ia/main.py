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
from goals import goalsManager

Constantes = constantes.Constantes()
ObjetCommunication = communicationGlobale.CommunicationGlobale(Constantes)
arduino_constantes = ObjetCommunication.getConst()
gManager = goalsManager.GoalsManager()
gManager.getBestGoal([1,1])
gManager.saveGoals()

time.sleep(1000/1000.0)
print("INFO: La communication est prête")
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
