# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys

#Nos fichiers
from communication import communicationGlobale
import pullData
import guiCommande


#objetCommunication = communicationGlobale.communicationGlobale("/dev/ttyUSB0", 57600, "ODD", "/dev/ttymxc3", 115200, "NONE", "/dev/ttyACM0", 115200, "NONE")
objetCommunication = None
objetPullData = pullData.pullData(objetCommunication)

try:
	while True:
		pass
except KeyboardInterrupt:
	#objetCommunication.stopGestion()
	pass
finally:
	#objetCommunication.stopGestion()
	pass
