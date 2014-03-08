# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys
import time
import logging

#logfile_name = "log/" + time.strftime("%d %b %Y %H:%M:%S", time.gmtime()) + ".log"
logging.basicConfig(filename="log/last.log", filemode='w', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__.split('.')[0])


#Nos fichiers
import communication
import data
from constantes import *
import event
import timeManager

logger.info("Demarrage de l'ia")
Communication = communication.CommunicationGlobale()
arduino_constantes = Communication.getConst()
time.sleep(0.5) # on attend que les communications s'établissent

#On teste si les systèmes demandés sont bien en lignes
ready_list = Communication.getSystemReady()
if ENABLE_FLUSSMITTEL and ( ('ADDR_FLUSSMITTEL_OTHER' not in ready_list) or ('ADDR_FLUSSMITTEL_ASSERV' not in ready_list) ):
	logger.critical("ERREUR: Incohérence de communication avec le gros robot, ENABLE_FLUSSMITTEL: " + str(ENABLE_FLUSSMITTEL) + " ready_list: " + str(ready_list))
	exit()
if ENABLE_TIBOT and ( ('ADDR_TIBOT_OTHER' not in ready_list) or ('ADDR_TIBOT_ASSERV' not in ready_list) ):
	logger.critical("ERREUR: Incohérence de communication avec le petit robot, ENABLE_TIBOT: " + str(ENABLE_TIBOT) + " ready_list: " + str(ready_list))
	exit()
if ENABLE_TOURELLE and 'ADDR_HOKUYO' not in ready_list:
	logger.critical("ERREUR: Incohérence de communication avec le petit robot, ENABLE_TOURELLE: " + str(ENABLE_TOURELLE) + " ready_list: " + str(ready_list))
	exit()
logger.info("Les systèmes attendu ont bien été détéctés. Flussmittel: %s   Tibot: %s   Tourelle: %s   ready_list: %s", ENABLE_FLUSSMITTEL, ENABLE_TIBOT, ENABLE_TOURELLE, ready_list)


Data = data.Data(Communication, arduino_constantes)
EventManager = event.EventManager(Data)
TimeManager = timeManager.TimeManager(Data.MetaData)



#TODO if jack ready
TimeManager.startMatch()
