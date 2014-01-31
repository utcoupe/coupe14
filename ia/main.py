# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys

#Nos fichiers
from communication import communicationGlobale
import guiCommande

com = communicationGlobale.communicationGlobale("/dev/ttyUSB0", 57600, "ODD", "/dev/ttymxc3", 115200, "NONE", "/dev/ttyACM0", 115200, "NONE")

try:
	guiCommande.gui(com)

except KeyboardInterrupt:
	com.stopGestion()
finally:
	com.stopGestion()
