# -*- coding: utf-8 -*-
"""
Ce fichier gère la communication
"""

from collections import deque

import parser_c
import serial_comm


class Communication():
	def __init__(self, port):
		#on récupère les constantes
		self.address = {}
		self.orders = {}
		self.ordersSize = {}
		self.ordersListBuffer = deque()


		(self.address, self.orders, self.ordersSize) = parser_c.parseConstante()
		#on initialise le port serial du xbee explorer
		self.liaisonXbee = serial_comm.ComSerial(port, 57600)

	def getConst():
		return (self.address, self.orders, self.ordersSize)

	def extractData(self, rawInput):
		""" prend rawInput une chaine de caractère qui correspond  qui correspond à un ordre, retourne les autres packerData est prêt à être interpréter"""

		packetAddress = ord(rawInput[0]) - 128
		packetId = ord(rawInput[1])
		rawInput = rawInput[2:-1] # on supprime les deux carctère du dessus et le paquet de fin
		
		#python enleve les zero lors de la conversion en binaire donc on les rajoute, sauf le premier du protocole
		packetData = ""
		for octet in rawInput:
			temp = bin(ord(octet))[2:]
			while len(temp) < 7:
				temp = '0' + temp
			packetData += temp

		return (packetAddress, packetId, packetData)

	def getXbeeOrders(self):
		""" retourne ordersList, une liste d'élements sous la forme(adresse, id, data) où data est prêt à être interpréter"""
		rawInputList = self.liaisonXbee.read()

		ordersList = deque()

		for rawInput in rawInputList:
			ordersList.append(self.extractData(rawInput))

		for order in ordersList:
			print(order[0])
			print(order[1])
			for i in range(0, len(order[2]), 8):
				if int(order[2][i:i+8], 2):
					print("data: " + chr(int(order[2][i:i+8], 2)))

		return ordersList


	def readOrders(self):
		ordersList = deque()
		print(self.getXbeeOrders())


	#Envoi
	def applyProtocole(self, address, packetId, data):
		""" on concatène les trois parametres et on retourne chaineRetour en appliquant le protocole """
		chaineRetour = ""
		chaineRetour += chr(address + 128)
		chaineRetour += chr(packetId)

		#on ajoute les data
		rawBinary = ""
		for octet in data:
			rawBinary += bin(ord(octet))[2:].zfill(8)
		while len(rawBinary)%7!=0: # hack pour former correctement le dernier octet
			rawBinary += '0'
		for i in range(0, len(rawBinary), 7):
			chaineRetour += chr(int(rawBinary[i:i+7], 2))
		
		#on ajoute l'octet de fin
		chaineRetour += chr(128)

		return(chaineRetour)


	def sendXbeeOrders(self, ordersList):
		""" ordersList est une liste de chaine de caractère sous la forme (adresse, id, data) où data est une chaine de char avec un ou plusieurs ordres"""
		for order in ordersList:
			chaineTemp = self.applyProtocole(order[0], order[1], order[2])
			self.liaisonXbee.send(chaineTemp)


	def addOrders(self, order):
		""" order est de la forme (adresse, id, data) où data ne contient d'un ordre, on ajoute l'ordre dans ordersListBuffer """
		# on lis les ordres et on les regroupes par detination
		self.ordersListBuffer.append(order)


instance = Communication("/dev/ttyUSB0")
instance2 = Communication("/dev/ttyUSB1")

ordersList = deque()

import time
while 1:
	address = int(raw_input("Entre une adresse (int)"))
	idd = int(raw_input("Entre un id (int)"))
	data = str(raw_input("Entre le nom d'un ordre (string)"))
	print(instance.getConst()[2])

	ordersList.append((address,idd,data))
	instance.sendXbeeOrders(ordersList)
	ordersList.pop()

	time.sleep(1)
	instance2.getXbeeOrders()

