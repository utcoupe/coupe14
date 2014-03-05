# -*- coding: utf-8 -*-
"""
Fichier principale, demarre l'ia
"""

#Libs
import sys
import time

#Nos fichiers
import constantes
from communication import communicationGlobale
from data import data
from goals import goalsManager
import gestionTemps

ObjetCommunication = communicationGlobale.CommunicationGlobale(constantes)
arduino_constantes = ObjetCommunication.getConst()
time.sleep(2) # on attend que les communications s'établissent


#On teste si les systèmes demandés sont bien en lignes
ready_list = ObjetCommunication.getSystemReady()
if constantes.ENABLE_FLUSSMITTEL and ( ('ADDR_FLUSSMITTEL_OTHER' not in ready_list) or ('ADDR_FLUSSMITTEL_ASSERV' not in ready_list) ):
	print("ERREUR: Incohérence de communication avec le gros robot, ENABLE_FLUSSMITTEL:", constantes.ENABLE_FLUSSMITTEL, "USE_ARDUINO:",constantes.USE_ARDUINO,"ready_list:", ready_list)
	exit()
if constantes.ENABLE_TIBOT and ( ('ADDR_TIBOT_OTHER' not in ready_list) or ('ADDR_TIBOT_ASSERV' not in ready_list) ):
	print("ERREUR: Incohérence de communication avec le petit robot, ENABLE_TIBOT:", constantes.ENABLE_TIBOT, "USE_XBEE:",constantes.USE_XBEE,"ready_list:", ready_list)
	exit()
if constantes.ENABLE_TOURELLE and 'ADDR_HOKUYO' not in ready_list:
	print("ERREUR: Incohérence de communication avec le petit robot, ENABLE_TIBOT:", constantes.ENABLE_TIBOT, "USE_XBEE:",constantes.USE_XBEE,"ready_list:", ready_list)
	exit()
print("Le protocole a bien demarré.")


Data = data.Data(ObjetCommunication, constantes, arduino_constantes)
GoalsManager = goalsManager.GoalsManager()
GestionTemps = gestionTemps.GestionTemps(Data)
