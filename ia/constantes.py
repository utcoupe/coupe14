# -*- coding: utf-8 -*-
"""
Ce fichier regroupe toutes les constantes de l'IA
"""

class constantes():
	def __init__(self):
		#====================Jeu====================
		self.numberOfenemy = 0




		#====================Communication====================
		self.portXbee = "/dev/ttyUSB0"
		self.vitesseXbee = 57600
		self.parityXbee = "ODD"
		self.portOther = "/dev/ttymxc3"
		self.vitesseOther = 115200
		self.parityOther = "NONE"


		#constantes réglables:
		self.useXbee = True
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


		#====================pullData====================
		self.pullPeriode = 50 #période des pull en ms

		#====================CAMERA====================
		self.seuilRouge = 100 #TODO
		self.seuilJaune = 100 #TODO

		#====================FM====================
		self.largeurFM = 100 #en mm
		self.longueurFM = 100








		#====================TIBOT====================
		self.largeurTB = 100
		self.longueurTB = 100





		#====================BIG ENEMY====================
		#Si un seul adversaire, on utilise les constantes de BIG ENEMY
		self.largeurBigEnemy = 100
		self.longueurBigEnemy = 100



		#====================SMALL ENEMY====================
		self.largeurSmallEnemy = 100
		self.longueurSmallEnemy = 100
