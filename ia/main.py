# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import threading
import sys



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
finally:
	com.stopGestion()
	#print "Unexpected error:", sys.exc_info()[0]