# -*- coding: utf-8 -*-
"""
Ce fichier regroupe toutes les constantes de l'IA
"""

class Constantes():
	def __init__(self):
		#========================================Communication========================================
		self.portXbee = "/dev/ttyUSB0"
		self.vitesseXbee = 57600
		self.parityXbee = "ODD"
		self.portOther = "/dev/ttymxc3"
		self.vitesseOther = 115200
		self.parityOther = "NONE"


		#constantes réglables:
		self.useXbee = False
		self.useArduino = True
		self.maxUnconfirmedPacket = 5 # attention maximum 32
		self.emptyFifo = True
		self.timeOut = 100
		self.highPrioSpeed = 30 #période d'execution en ms
		self.lowPrioSpeed = 1000 #période d'execution en ms
		self.keepContactTimeout = 1000
		self.offLigneTimeout = 5000

		#Systèmes arretable:
		self.threadActif = True
		self.writeOutput = True
		self.readInput = True
		self.probingDevices = True
		self.renvoiOrdre = True
		self.keepContact = True
		self.renvoiImmediat = False # fonction non terminé, ne pas activer !


		#=======================================IA========================================
		
		#====================Variables globales====================
		self.number_of_enemy = 0




		
		#====================tourelle====================
		self.enable_tourelle = False #permet de deactiver la tourelle

		#====================pullData====================
		self.pull_periode = 50 #période des pull en ms

		#====================CAMERA====================
		self.seuil_rouge = 100 #TODO
		self.seuil_jaune = 100 #TODO

		#====================Flussmittel====================
		self.enable_flussmittel = True #permet de deactiver Flussmitel
		self.largeur_flussmittel = 100 #en mm
		self.longueur_flussmittel = 100








		#====================TIBOT====================
		self.enable_tibot = False #permet de deactiver un Tibot
		self.largeur_tibot = 100
		self.longueur_tibot = 100





		#====================BIG ENEMY====================
		#Si un seul adversaire, on utilise les constantes de BIG ENEMY
		self.largeurBigEnemy = 100
		self.longueurBigEnemy = 100



		#====================SMALL ENEMY====================
		self.largeurSmallEnemy = 100
		self.longueurSmallEnemy = 100
