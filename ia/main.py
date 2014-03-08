# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys
import time
import logging

#logfile_name = "log/" + time.strftime("%d %b %Y %H:%M:%S", time.gmtime()) + ".log"
logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "log/last.log"), filemode='w', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__.split('.')[0])


#Nos fichiers
import communication
import data
from constantes import *

logger.info("Demarrage de l'ia")
Communication = communication.CommunicationGlobale()
arduino_constantes = Communication.getConst()
time.sleep(0.5) # on attend que les communications s'établissent

#On teste si les systèmes demandés sont bien en lignes
ready_list = Communication.getSystemReady()
if ENABLE_FLUSSMITTEL and ( ('ADDR_FLUSSMITTEL_OTHER' not in ready_list) or ('ADDR_FLUSSMITTEL_ASSERV' not in ready_list) ):
	logger.cirtical("ERREUR: Incohérence de communication avec le gros robot, ENABLE_FLUSSMITTEL:", constantes.ENABLE_FLUSSMITTEL, "USE_ARDUINO:",constantes.USE_ARDUINO,"ready_list:", ready_list)
	exit()
if ENABLE_TIBOT and ( ('ADDR_TIBOT_OTHER' not in ready_list) or ('ADDR_TIBOT_ASSERV' not in ready_list) ):
	logger.cirtical("ERREUR: Incohérence de communication avec le petit robot, ENABLE_TIBOT:", constantes.ENABLE_TIBOT, "USE_XBEE:",constantes.USE_XBEE,"ready_list:", ready_list)
	exit()
if ENABLE_TOURELLE and 'ADDR_HOKUYO' not in ready_list:
	logger.cirtical("ERREUR: Incohérence de communication avec le petit robot, ENABLE_TIBOT:", constantes.ENABLE_TIBOT, "USE_XBEE:",constantes.USE_XBEE,"ready_list:", ready_list)
	exit()
logger.info("Les systèmes attendu ont bien été détéctés. Flussmittel: %s   Tibot: %s   Tourelle: %s", ENABLE_FLUSSMITTEL, ENABLE_TIBOT, ENABLE_TOURELLE)


Data = data.Data(Communication, arduino_constantes)
#On l'instanciera depuis eventManager
#GoalsManager = goals.GoalsManager()

