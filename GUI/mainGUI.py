"""
Fichier principale, demarre l'ia
"""

#Libs
import sys
import os
import time

lib_path = os.path.abspath('./ia')
sys.path.append(lib_path)

#Nos fichiers
from communication import communicationGlobale
from data import data
import constantes

Constantes = constantes.Constantes()
ObjetCommunication = communicationGlobale.CommunicationGlobale(Constantes)
arduino_constantes = ObjetCommunication.getConst()

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
