#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys
import os
import time
import logging

#logfile_name = "log/" + time.strftime("%d %b %Y %H:%M:%S", time.gmtime()) + ".log"



#Nos fichiers
import communication
import data
from constantes import *
import event
import gpio

#lancement de l'IA via le subprocess simu
def startIa(pipe=None, ia_color="RED"):
	Communication = communication.CommunicationGlobale()
	arduino_constantes = Communication.getConst()

	logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "log/last_"+str(ia_color)+".log"), filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	logger = logging.getLogger(__name__.split('.')[0])

	if pipe == None:
		logger.info("Demarrage d'une IA normal")
		time.sleep(2) # on attend que les communications s'établissent

		if TEST_MODE == False:
			#On teste si les systèmes demandés sont bien en lignes
			ready_list = Communication.getSystemReady()
			if ENABLE_FLUSSMITTEL == True and ( ('ADDR_FLUSSMITTEL_OTHER' not in ready_list) or ('ADDR_FLUSSMITTEL_ASSERV' not in ready_list) ):
				logger.critical("ERREUR: Incohérence de communication avec le gros robot, le systeme suivant a été demandé mais pas trouvé: ENABLE_FLUSSMITTEL: " + str(ENABLE_FLUSSMITTEL) + " ready_list: " + str(ready_list))
				exit()
			if ENABLE_TIBOT == True and ( ('ADDR_TIBOT_OTHER' not in ready_list) or ('ADDR_TIBOT_ASSERV' not in ready_list) ):
				logger.critical("ERREUR: Incohérence de communication avec le petit robot, le systeme suivant a été demandé mais pas trouvé: ENABLE_TIBOT: " + str(ENABLE_TIBOT) + " ready_list: " + str(ready_list))
				exit()
			if ENABLE_TOURELLE ==  True and 'ADDR_HOKUYO' not in ready_list:
				logger.critical("ERREUR: Incohérence de communication avec la tourelle, le systeme suivant a été demandé mais pas trouvé: ENABLE_TOURELLE: " + str(ENABLE_TOURELLE) + " ready_list: " + str(ready_list))
				exit()
			logger.info("Les systèmes attendu ont bien été détéctés. Flussmittel: %s   Tibot: %s   Tourelle: %s   ready_list: %s", ENABLE_FLUSSMITTEL, ENABLE_TIBOT, ENABLE_TOURELLE, ready_list)
		else:
			print("---------------------TEST_MODE activé---------------------")
			logger.warning("----------------------------------------TEST_MODE activé----------------------------------------")

	else:
		logger.info("Demarrage d'une IA depuis le simuateur")
		Communication = communication.CommSimulateur(pipe) #TODO remplacer par un emulateur de READAPI et SENDAPI en utilisant conn



	Data = data.Data(Communication, arduino_constantes)
	if TEST_MODE == False and ENABLE_FLUSSMITTEL == True:
		Gpio = gpio.Gpio()
		data.parametrerHokuyo()
		data.parametrerIa(Data.MetaData, Gpio.getColor)
	else:
		data.parametrerHokuyo()
		data.parametrerIa(Data.MetaData, ia_color)

	TimeManager = event.TimeManager(Communication, Data)
	EventManager = event.EventManager(Communication, Data)



	if TEST_MODE == False and ENABLE_FLUSSMITTEL == True:
		while Gpio.getJack() != True: #TODO à verifier
			pass
	TimeManager.startMatch()

#si on lance l'IA via le main.py
if __name__ == "__main__":
	startIa()