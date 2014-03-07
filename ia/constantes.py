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
HIGH_PRIO_SPEED = 		30 #période d'execution en ms
LOW_PRIO_SPEED = 		1000 #période d'execution en ms
KEEP_CONTACT_TIMEOUT = 	1000
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





#====================tourelle====================
ENABLE_TOURELLE = 		False #permet de deactiver la tourelle

#====================pullData====================
PULL_PERIODE = 			50 #période des pull en ms

#====================CAMERA====================
SEUIL_ROUGE = 			100 #TODO
SEUIL_JAUNE = 			100 #TODO

#====================Flussmittel====================
ENABLE_FLUSSMITTEL = 	False #permet de deactiver Flussmitel
LARGEUR_FLUSSMITTEL = 	100
LONGUEUR_FLUSSMITTEL = 	100
RAYON_FLUSSMITTEL = 	math.sqrt(LARGEUR_FLUSSMITTEL * LARGEUR_FLUSSMITTEL + LONGUEUR_FLUSSMITTEL * LONGUEUR_FLUSSMITTEL) #en mm









#====================TIBOT====================
ENABLE_TIBOT = 			True #permet de deactiver un Tibot
LARGEUR_TIBOT = 		100
LONGUEUR_TIBOT = 		100
RAYON_TIBOT = 			math.sqrt(LARGEUR_TIBOT * LARGEUR_TIBOT + LONGUEUR_TIBOT * LONGUEUR_TIBOT) 





#====================BIG ENEMY====================
#Si un seul adversaire, on utilise les constantes de BIG ENEMY
RAYON_BIG_ENEMY = 		100




#====================SMALL ENEMY====================
RAYON_SMALL_ENEMY = 	100

#=======================================IA========================================
POINTS_PAR_CERCLE = 8
MARGE_PASSAGE = 10
