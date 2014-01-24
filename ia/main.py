# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import threading

#Nos fichiers
from communication import communicationGlobale
import guiCommande

com = communicationGlobale.communicationGlobale("/dev/ttyUSB0")
gestionThread = threading.Thread(target=com.gestion)


try:
	gestionThread.start()
	guiCommande.gui(com)
except KeyboardInterrupt:
	com.stopGestion()