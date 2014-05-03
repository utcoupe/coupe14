# -*- coding: utf-8 -*-
"""
Ce fichier regroupe toutes les constantes de l'IA
"""


TEST_MODE = False #Permet des tester l'IA sans avoir besoin d'être connecté aux robots




#====================Enable====================
ENABLE_TOURELLE = 		False
ENABLE_FLUSSMITTEL = 	True #permet de desactiver Flussmitel
ENABLE_TIBOT = 			False

#========================================Communication========================================
PORT_XBEE = 			"/dev/ttyUSB0"
VITESSE_XBEE = 			57600
PARITY_XBEE = 			"ODD"
PORT_OTHER = 			"/dev/ttyACM0"
VITESSE_OTHER = 		57600
PARITY_OTHER = 			"ODD"


#constantes réglables:
MAX_UNCONFIRMED_PACKET =5 # maximum 32
TIMEOUT = 				100
HIGH_PRIO_SPEED = 		2 #période d'execution en ms
LOW_PRIO_SPEED = 		3000 #période d'execution en ms
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
NUMBER_OF_ENEMY = 		2 #TODO

#====================eventManager====================
PERIODE_EVENT_MANAGER =	2
ID_ACTION_MAX =			29999

#====================timeManager====================
PERIODE_TIME_MANAGER =	100
END_OF_MATCH = 			89500
BEGIN_FUNNY_ACTION =	90000
END_OF_FUNNY_ACTION = 	94000
BEGIN_CHECK_COLLISION =	3000 #TODO

#====================Goal====================
FINISHED_THRESHOLD = 	50

#====================pullData====================
PULL_PERIODE = 			10 #période des pull en ms


#====================NAVIGATION================
EMPTY_FIFO = 			True
POINTS_PAR_CERCLE = 	8
MARGE_PASSAGE_PATH = 	0
MARGE_COLLISION =		-20
COLLISION_THRESHOLD =	150


#=======================================Systemes physiques========================================
#====================tourelle====================
OUR_ROBOTS_VISIBLE_TOURELLE = True 	#True si une balise visible par l'hokuyo est presente sur nos robots 
TOURELLE_PULL_PERIODE = 100 		#ms

#====================Flussmittel====================
LARGEUR_FLUSSMITTEL = 	330
LONGUEUR_FLUSSMITTEL = 	260
MAX_FRONT_TRIANGLE_STACK = 3
MAX_BACK_TRIANGLE_STACK = 1
GARDE_AU_SOL = 16
HAUTEUR_TRIANGLE = 30
MARGE_DROP_TRIANGLE = 0
HAUTEUR_TORCHE = 36

#====================TIBOT====================
LARGEUR_TIBOT = 		200
LONGUEUR_TIBOT = 		150

#====================BIG ENEMY====================
#Si un seul adversaire, on utilise les constantes de BIG ENEMY
RAYON_BIG_ENEMY = 		200

#====================SMALL ENEMY====================
RAYON_SMALL_ENEMY = 	120

