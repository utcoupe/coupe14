# -*- coding: utf-8 -*-
"""
Ce fichier regroupe toutes les constantes de l'IA
"""

#========================================Communication========================================
portXbee = "/dev/ttyUSB0"
vitesseXbee = 57600
parityXbee = "ODD"
portOther = "/dev/ttymxc3"
vitesseOther = 115200
parityOther = "NONE"


#constantes réglables:
useXbee = False
useArduino = False
maxUnconfirmedPacket = 5 # attention maximum 32
emptyFifo = True
timeOut = 100
highPrioSpeed = 30 #période d'execution en ms
lowPrioSpeed = 1000 #période d'execution en ms
keepContactTimeout = 1000
offLigneTimeout = 5000

#Systèmes arretable:
threadActif = True
writeOutput = True
readInput = True
probingDevices = True
renvoiOrdre = True
keepContact = True
renvoiImmediat = False # fonction non terminé, ne pas activer !


#=======================================IA========================================

#====================Variables globales====================
NUMBER_OF_ENEMY = 0





#====================tourelle====================
ENABLE_TOURELLE = False #permet de deactiver la tourelle

#====================pullData====================
PULL_PERIODE = 50 #période des pull en ms

#====================CAMERA====================
SEUIL_ROUGE = 100 #TODO
SEUIL_JAUNE = 100 #TODO

#====================Flussmittel====================
ENABLE_FLUSSMITTEL = True #permet de deactiver Flussmitel
LARGEUR_FLUSSMITTEL = 100 #en mm
LONGUEUR_FLUSSMITTEL = 100








#====================TIBOT====================
ENABLE_TIBOT = False #permet de deactiver un Tibot
LARGEUR_TIBOT = 100
LONGUEUR_TIBOT = 100





#====================BIG ENEMY====================
#Si un seul adversaire, on utilise les constantes de BIG ENEMY
LARGEUR_BIG_ENEMY = 100
LONGUEUR_BIG_ENEMY = 100



#====================SMALL ENEMY====================
LARGEUR_SMALL_ENEMY = 100
LONGUEUR_SMALL_ENEMY = 100
