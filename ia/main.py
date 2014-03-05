# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys
import time

#Nos fichiers
import communication
import data
import constantes
import goals

ObjetCommunication = communication.CommunicationGlobale()
arduino_constantes = ObjetCommunication.getConst()
goalsManager = goals.GoalsManager()

time.sleep(1000/1000.0)
print("INFO: La communication est prête")
data = data.Data(ObjetCommunication, arduino_constantes)

try:
	while True:
		time.sleep(1000/1000.0)
except KeyboardInterrupt:
	pass
finally:
	pass
