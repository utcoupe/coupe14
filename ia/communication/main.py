# -*- coding: utf-8 -*-
"""
Ce fichier gère la communication
"""

from collections import deque
import struct

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
		self.lastIdConfirm = {x:63 for x in self.address}
		self.lastIdSend = self.lastIdConfirm

		self.liaisonXbee = serial_comm.ComSerial(port, 57600)

	def getConst(self):
		return (self.address, self.orders, self.ordersSize)

	def getId(self, address):
		"""retourne l'id qu'il faut utiliser pour envoyer un packet à l'adresse passé en argument"""
		if self.lastIdSend[address] >= 63:# -1 car l'adresse 0 n'existe pas
			return 0
		else:
			self.lastIdSend[address] += 1
			return self.lastIdSend[address]








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

		print("raw")
		print(packetData)
		return (packetAddress, packetId, packetData)

	def getXbeeOrders(self):
		""" retourne ordersList, une liste d'élements sous la forme(adresse, id, data) où data est prêt à être interpréter"""
		rawInputList = self.liaisonXbee.read()

		ordersList = deque()

		for rawInput in rawInputList:
			ordersList.append(self.extractData(rawInput))

		return ordersList


	def readOrders(self):
		ordersList = self.getXbeeOrders()

		for order in ordersList:
			address =order[0]
			idd = order[1]

			index = 0
			orderNumber = int(order[2][index:6], 2)
			index += 6
			orderSize = instance.getConst()[2][ instance.getConst()[1][ orderNumber ] ]
			for i in range(index, orderSize*8+index, 8):
				print("data: ")
				temp2 = ""
				for b in range(8, 0, -1):
					temp2 += order[2][i - b + 1]
				print(int(temp2, 2)) 





	#Envoi
	def applyProtocole(self, address, packetId, data):
		""" on concatène les trois parametres et on retourne chaineRetour en appliquant le protocole """
		chaineRetour = ""
		chaineRetour += chr(address + 128)
		chaineRetour += chr(packetId)

		rawBinary = data
		
		while len(rawBinary)%7!=0: # hack pour former correctement le dernier octet
			rawBinary += '0'
		for i in range(0, len(rawBinary), 7):
			chaineRetour += chr(int(rawBinary[i:i+7], 2))
		
		#on ajoute l'octet de fin
		chaineRetour += chr(128)

		print("send raw")
		print(rawBinary)
		return(chaineRetour)


	def sendXbeeOrders(self, ordersList):
		""" ordersList est une liste de chaine de caractère sous la forme (adresse, id, data) où data est une chaine de char avec un ou plusieurs ordres"""
		for order in ordersList:
			chaineTemp = self.applyProtocole(order[0], order[1], order[2])
			self.liaisonXbee.send(chaineTemp)

	def sendOrder(self, order):
		"""c'est la fonction que l'utilisateur doit manipuler, ordre est de type (address, data)"""
		#TODO:
		#on get les packet à renvoyer
		#on y ajoute notre packet
		#on envoye tout à sendXbeeOrders

		#bypass temporaire:
		ordersList = deque()
		ordersList.append((order[0], self.getId(order[0]), order[1]))
		self.sendXbeeOrders(ordersList)
		ordersList.pop()



def floatToBinary(num):
	"""retourne une chaine de 32 bits"""
	return ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))

def intToBinary(num):
	"""retourne une chaine de 16 bits"""
	temp2 = ""
	temp = bin(num)[2:]
	while len(temp) < 16:
		temp = '0' + temp
	for i in range(8, 0, -1):
		temp2 += temp[i-1]
	for i in range(16, 8, -1):
		temp2 += temp[i-1]
	return temp2

def orderToBinary(num):
	"""retourne une chaine de 6 bits"""
	temp = bin(num)[2:]
	while len(temp) < 6:
		temp = '0' + temp
	return temp




instance = Communication("/dev/ttyUSB0")
import time
while 1:
	dataString = str(raw_input("Entre le nom d'un ordre (string)"))
	if dataString == 'A_GOTO':
		data = orderToBinary(int(instance.getConst()[1][dataString]))
		data += intToBinary(int(raw_input("Entre l'argument 1 (int)")))
		data += intToBinary(int(raw_input("Entre l'argument 2 (int)")))

	elif dataString == 'A_ROT':
		data = orderToBinary(instance.getConst()[1][dataString])
		data += floatToBinary(float(raw_input("Entre l'argument 1 (float)")))

	elif dataString == 'A_PWM_TEST':
		data = orderToBinary(int(instance.getConst()[1][dataString]))
		data += intToBinary(int(raw_input("Entre l'argument 1 (int)")))
		data += intToBinary(int(raw_input("Entre l'argument 2 (int)")))
		data += intToBinary(int(raw_input("Entre l'argument 3 (int)")))

	elif dataString == 'A_PIDA':
		data = orderToBinary(int(instance.getConst()[1][dataString]))
		data += intToBinary(int(raw_input("Entre l'argument 1 (int)")))
		data += intToBinary(int(raw_input("Entre l'argument 2 (int)")))
		data += intToBinary(int(raw_input("Entre l'argument 3 (int)")))

	elif dataString == 'A_PIDD':
		data = orderToBinary(int(instance.getConst()[1][dataString]))
		data += intToBinary(int(raw_input("Entre l'argument 1 (int)")))
		data += intToBinary(int(raw_input("Entre l'argument 2 (int)")))
		data += intToBinary(int(raw_input("Entre l'argument 3 (int)")))

	elif dataString == 'PINGPING':
		data = orderToBinary(int(instance.getConst()[1][dataString]))

	elif dataString == 'A_GET_CODER':
		data = orderToBinary(int(instance.getConst()[1][dataString]))

	else:
		print ("L'ordre n'est pas implementé")

	address = 2
	instance.sendOrder((address,data))
	

