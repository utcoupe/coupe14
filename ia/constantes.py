# -*- coding: utf-8 -*-
"""
Ce fichier regroupe toutes les constantes de l'IA
"""


DEBUG_MODE = True




#====================Enable====================
ENABLE_TOURELLE = 		True 
ENABLE_FLUSSMITTEL = 	True #permet de desactiver Flussmitel
ENABLE_TIBOT = 			True

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
HIGH_PRIO_SPEED = 		2 #période d'execution en ms
LOW_PRIO_SPEED = 		400 #période d'execution en ms
KEEP_CONTACT_TIMEOUT = 	1500
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
PERIODE_EVENT_MANAGER =	20
ID_ACTION_MAX =			29999

#====================timeManager====================
PERIODE_TIME_MANAGER =	100
END_OF_MATCH = 			89500
BEGIN_FUNNY_ACTION =	90000
END_OF_FUNNY_ACTION = 	94000
BEGIN_CHECK_COLLISION =	3000 #TODO

#====================Goal====================
FINISHED_THRESHOLD = 50


#====================tourelle====================
OUR_ROBOTS_VISIBLE_TOURELLE = True 	#True si une balise visible par l'hokuyo est presente sur nos robots 
TOURELLE_PULL_PERIODE = 100 		#ms

#====================pullData====================
PULL_PERIODE = 			10 #période des pull en ms

#====================CAMERA====================
SEUIL_ROUGE = 			100 #TODO
SEUIL_JAUNE = 			100 #TODO

#====================Flussmittel====================
LARGEUR_FLUSSMITTEL = 	100
LONGUEUR_FLUSSMITTEL = 	100





#====================TIBOT====================
LARGEUR_TIBOT = 		100
LONGUEUR_TIBOT = 		100




#====================BIG ENEMY====================
#Si un seul adversaire, on utilise les constantes de BIG ENEMY
RAYON_BIG_ENEMY = 		100




#====================SMALL ENEMY====================
RAYON_SMALL_ENEMY = 	100

#=======================================IA========================================
#====================NAVIGATION================
POINTS_PAR_CERCLE = 8
MARGE_PASSAGE_PATH = 10
