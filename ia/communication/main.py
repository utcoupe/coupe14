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
		self.sendId = 0
		self.receiveId = 0


		(self.address, self.orders, self.ordersSize) = parser_c.parseConstante()
		#on initialise le port serial du xbee explorer
		self.liaisonXbee = serial_comm.ComSerial(port, 57600)

	def getConst(self):
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
		ordersList = deque()
		#print(self.getXbeeOrders())


	#Envoi
	def applyProtocole(self, address, packetId, data):
		""" on concatène les trois parametres et on retourne chaineRetour en appliquant le protocole """
		chaineRetour = ""
		chaineRetour += chr(address + 128)
		chaineRetour += chr(self.sendId)
		self.sendId += 1

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


	def addOrders(self, order):
		""" order est de la forme (adresse, id, data) où data ne contient d'un ordre, on ajoute l'ordre dans ordersListBuffer """
		# on lis les ordres et on les regroupes par detination
		self.ordersListBuffer.append(order)


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
#instance2 = Communication("/dev/ttyUSB1")

ordersList = deque()
ordersList2 = deque()

import time
while 1:
	address = int(raw_input("Entre une adresse (int)"))
	idd = int(raw_input("Entre un id (int)"))

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

	else:
		print ("L'ordre n'est pas implementé")

	ordersList.append((address,idd,data))
	instance.sendXbeeOrders(ordersList)
	ordersList.pop()
	"""

	time.sleep(1)
	ordersList2 = instance.getXbeeOrders()


	for order in ordersList2:
		print("BEGIN")
		print(order[0])
		print(order[1])

		index = 0
		orderNumber = int(order[2][index:6], 2)
		index += 6
		orderSize = instance.getConst()[2][ instance.getConst()[1][ orderNumber ] ]
		for i in range(index, orderSize*8+index, 8):
			print("data: ")
			print(int(order[2][i:i+8], 2)) """

