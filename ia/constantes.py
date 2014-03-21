# -*- coding: utf-8 -*-
"""
Ce fichier regroupe toutes les constantes de l'IA
"""

import math

#========================================Communication========================================
PORT_XBEE = 			"/dev/ttyUSB0"
VITESSE_XBEE = 			57600
PARITY_XBEE = 			"ODD"
PORT_OTHER = 			"/dev/ttymxc3"
VITESSE_OTHER = 		115200
PARITY_OTHER = 			"NONE"


#constantes réglables:
MAX_UNCONFIRMED_PACKET =5 # maximum 32
EMPTY_FIFO = 			True
TIMEOUT = 				100
HIGH_PRIO_SPEED = 		20 #période d'execution en ms
LOW_PRIO_SPEED = 		1000 #période d'execution en ms
KEEP_CONTACT_TIMEOUT = 	2000
OFF_LIGNE_TIMEOUT = 	5000

#Systèmes arretable:
THREAD_ACTIF = 			True
WRITE_OUTPUT = 			True
READ_INPUT = 			True
PROBING_DEVICES = 		True
RENVOI_ORDRE = 			True
KEEP_CONTACT = 			True
renvoiImmediat = 		False # fonction non terminé, ne pas activer !


#=======================================IA========================================

#====================Variables globales====================
NUMBER_OF_ENEMY = 		2

#====================eventManager====================
PERIODE_EVENT_MANAGER =	40
ID_ACTION_MAX =			29999

#====================timeManager====================
PERIODE_TIME_MANAGER =	100
END_OF_MATCH = 			89500
BEGIN_FUNNY_ACTION =	90000
END_OF_FUNNY_ACTION = 	94000

#====================tourelle====================
ENABLE_TOURELLE = 		False #permet de deactiver la tourelle

#====================pullData====================
PULL_PERIODE = 			100 #période des pull en ms

#====================CAMERA====================
SEUIL_ROUGE = 			100 #TODO
SEUIL_JAUNE = 			100 #TODO

#====================Flussmittel====================
ENABLE_FLUSSMITTEL = 	False #permet de deactiver Flussmitel
LARGEUR_FLUSSMITTEL = 	100
LONGUEUR_FLUSSMITTEL = 	100
RAYON_FLUSSMITTEL = 	math.sqrt(LARGEUR_FLUSSMITTEL * LARGEUR_FLUSSMITTEL + LONGUEUR_FLUSSMITTEL * LONGUEUR_FLUSSMITTEL) #en mm









#====================TIBOT====================
ENABLE_TIBOT = 			False #permet de deactiver un Tibot
LARGEUR_TIBOT = 		100
LONGUEUR_TIBOT = 		100
RAYON_TIBOT = 			math.sqrt(LARGEUR_TIBOT * LARGEUR_TIBOT + LONGUEUR_TIBOT * LONGUEUR_TIBOT) 





#====================BIG ENEMY====================
#Si un seul adversaire, on utilise les constantes de BIG ENEMY
RAYON_BIG_ENEMY = 		100




#====================SMALL ENEMY====================
RAYON_SMALL_ENEMY = 	100

#=======================================IA========================================
#====================NAVIGATION================
POINTS_PAR_CERCLE = 8
MARGE_PASSAGE_PATH = 10
