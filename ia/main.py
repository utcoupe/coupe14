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
from goals import goalsManager

ObjetCommunication = communicationGlobale.CommunicationGlobale(constantes)
arduino_constantes = ObjetCommunication.getConst()
gManager = goalsManager.GoalsManager()
gManager.getBestGoal([1,1])
gManager.saveGoals()

time.sleep(1000/1000.0)
print("INFO: La communication est prête")
data = data.Data(ObjetCommunication, constantes, arduino_constantes)

try:
	while True:
		time.sleep(1000/1000.0)
except KeyboardInterrupt:
	pass
finally:
	pass
