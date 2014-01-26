# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys

#Nos fichiers
from communication import communicationGlobale
import guiCommande

com = communicationGlobale.communicationGlobale("/dev/ttyUSB0")

try:
	guiCommande.gui(com)

except KeyboardInterrupt:
	com.stopGestion()
finally:
	com.stopGestion()