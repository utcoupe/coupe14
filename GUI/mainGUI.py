"""
Fichier principale, demarre l'ia
"""

#Libs
import sys
import os
import time

lib_path = os.path.abspath('../ia')
sys.path.append(lib_path)

#Nos fichiers
import communication
import data
import guiCommande

ObjetCommunication = communication.CommunicationGlobale()
ObjetCommunication.enableDebug()

time.sleep(1000/1000.0)
print("INFO: La communication est prête")
guiCommande.gui(ObjetCommunication)

try:
	while True:
		time.sleep(1000/1000.0)
except KeyboardInterrupt:
	#objetCommunication.stopGestion()
	pass
finally:
	#objetCommunication.stopGestion()
	pass
