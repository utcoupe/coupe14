# -*- coding: utf-8 -*-
"""
Ce fichier gère la communication
"""

from collections import deque
import struct
import time

import parser_c
import serial_comm


class CommunicationGobale():
	def __init__(self, port):
		#on récupère les constantes
		self.address = {}
		self.orders = {}
		self.ordersArguments = {}
		self.ordersRetour = {}
		self.ordersSize = {}
		(self.address, self.orders, self.ordersSize, self.ordersArguments, self.ordersRetour) = parser_c.parseConstante()
		self.checkTypeSize()
		
		self.arduinoIdReady = [False]*(len(self.address)+1)
		self.lastIdConfirm = {x:63 for x in self.address}
		self.lastIdSend = self.lastIdConfirm

		self.liaisonXbee = serial_comm.ComSerial(port, 57600)

		#defines de threads
		self.readInput = True
		self.probingIdReset = True


	def getConst(self):
		return (self.address, self.orders, self.ordersSize, self.ordersArguments, self.ordersRetour)

	def checkTypeSize(self):
		for order in self.orders:
			if not isinstance(order, (int)):# on teste uniquement les ordres numériques, ils sont identiquent aux strings
				sizeExpected = self.ordersSize[order]
				somme = 0
				for argumentType in self.ordersArguments[order]:
					if argumentType == 'int':
						somme += 2
					elif argumentType == 'long':
						somme += 4
					elif argumentType == 'float':
						somme += 4
					else:
						print("ERREUR: type parse inconnu")
				if somme != sizeExpected:
					print("ERREUR: la constante de taille de l'ordre ", order, " ne correspond pas aux types indiqués attendu ", sizeExpected, " calculee ", somme)
			
			





						#Gestion des id

	def getId(self, address):
		"""retourne l'id qu'il faut utiliser pour envoyer un packet à l'adresse passé en argument"""
		if self.lastIdSend[address] >= 63:# -1 car l'adresse 0 n'existe pas
			self.lastIdSend[address] = 0
		else:
			self.lastIdSend[address] += 1

		return self.lastIdSend[address]


	def askResetId(self, address): #demande a une arduino de reset
		chaineTemp = chr(address+192)
		self.liaisonXbee.send(chaineTemp)

	def probResetId(self):
		while self.probingIdReset == True:
			for address in range(1, len(self.address), 1):
				if self.arduinoIdReady[address] == False:
					self.askResetId(address)
			time.sleep(5)

	def stopProbResetId(self):
		self.probingIdReset = False


	#cas où on reçoi
	def acceptConfirmeResetId(self, address):#accepte la confirmation de reset d'un arduino
		print("accepte la confirmation de reset du systeme ", address)
		self.lastIdConfirm[address] = 63
		self.lastIdSend[address] = 63
		self.arduinoIdReady[address] = True

	def confirmeResetId(self, address):#renvoie une confirmation de reset
		print("renvoie une confirmation de reset du systeme ", address)
		self.lastIdConfirm[address] = 63
		self.lastIdSend[address] = 63
		chaineTemp = chr(address+224)
		self.liaisonXbee.send(chaineTemp)







	def extractData(self, rawInput):
		""" prend rawInput une chaine de caractère qui correspond  qui correspond à un ordre, retourne les autres packerData est prêt à être interpréter"""
		packetAddress = ord(rawInput[0]) - 128

		if packetAddress > 96:# l'arduino confirme le reset
			self.acceptConfirmeResetId(packetAddress-96)
			return 0

		elif packetAddress > 64:# l'arduino demande un reset
			self.confirmeResetId(packetAddress-64)
			return 0

		else:#cas normal
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
			ret = self.extractData(rawInput)
			if ret !=0:# 0 = cas du reset d'id
				ordersList.append(ret)

		return ordersList


	def readOrders(self):
		ordersList = self.getXbeeOrders()

		for order in ordersList:
			address = int(order[0])
			idd = int(order[1])

			if address in self.getConst()[0]:
				if idd >= 64:
					print("ERREUR: l'arduino", self.getConst()[0][address], " a mal recu un message id: ")

				else:
					print("success: l'arduino", self.getConst()[0][address]," a bien recu le message d'id: ", idd)
			else:
				print("ERREUR: address: ", address, " inconnue")
				

			"""index = 0
			orderNumber = int(order[2][index:6], 2)
			index += 6
			orderSize = self.getConst()[2][ self.getConst()[1][ orderNumber ] ]
			for i in range(index, orderSize*8+index, 8):
				print("data: ")
				temp2 = ""
				for b in range(8, 0, -1):
					temp2 += order[2][i - b + 1]
				print(int(temp2, 2)) """

	def stopReadingInput(self):
		self.readInput = False

	def lectureInput(self):
		while self.readInput == True:
			self.readOrders()
			time.sleep(0.1)


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
	temp = ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))
	temp2 = ""
	for i in range(24, 32, 1):
		temp2 += temp[i]
	for i in range(16, 24, 1):
		temp2 += temp[i]
	for i in range(8, 16, 1):
		temp2 += temp[i]
	for i in range(0, 8, 1):
		temp2 += temp[i]

	return temp2


def longToBinary(num):
	"""retourne une chaine de 32 bits"""
	temp2 = ""
	
	if num<0: #si l'int est négatif
		num = 4294967295 + num

	temp = bin(num)[2:]

	while len(temp) < 32:
		temp = '0' + temp

	#On inverse les 16 bits par blocks de 8, exemple AAAAAAAABBBBBBBB devient BBBBBBBBAAAAAAAA
	for i in range(24, 32, 1):
		temp2 += temp[i]
	for i in range(16, 24, 1):
		temp2 += temp[i]
	for i in range(8, 16, 1):
		temp2 += temp[i]
	for i in range(0, 8, 1):
		temp2 += temp[i]
	return temp2


def intToBinary(num):
	"""retourne une chaine de 16 bits"""
	temp2 = ""
	
	if num<0: #si l'int est négatif
		num = 65536 + num

	temp = bin(num)[2:]

	while len(temp) < 16:
		temp = '0' + temp

	#On inverse les 16 bits par blocks de 8, exemple AAAAAAAABBBBBBBB devient BBBBBBBBAAAAAAAA
	for i in range(8, 16, 1):
		temp2 += temp[i]
	for i in range(0, 8, 1):
		temp2 += temp[i]
	return temp2


def orderToBinary(num):
	"""retourne une chaine de 6 bits"""
	temp = bin(num)[2:]
	while len(temp) < 6:
		temp = '0' + temp
	return temp


def gui():
	while 1:
		dataString = str(raw_input("Entre le nom ou le numéro d'un ordre:"))
		address = 2

		if dataString == 'k':# arret d'urgence
			communication.sendOrder((address,orderToBinary(int(communication.getConst()[1]['A_KILLG']))))	
		elif dataString in communication.getConst()[1]:
			
			data = orderToBinary(int(communication.getConst()[1][dataString]))

			for typeToGet in communication.getConst()[3][dataString]:
				if typeToGet == 'int':
					data += intToBinary(int(raw_input("Entre  un int")))
				elif typeToGet == 'float':
					data += floatToBinary(float(raw_input("Entre un float")))
				elif typeToGet == 'long':
					data += intToBinary(long(raw_input("Entre  un long")))
				else:
					print("ERREUR: Parseur: le parseur un trouvé un type non supporté")
			communication.sendOrder((address,data))	
		else:
			print ("L'ordre n'a pas été trouvé dans les fichiers arduino")


communication = CommunicationGobale("/dev/ttyUSB0")


import threading
lectureInputThread = threading.Thread(target=communication.lectureInput)
probResetIdThread = threading.Thread(target=communication.probResetId)


try:
	lectureInputThread.start()
	probResetIdThread.start()
	gui()
except KeyboardInterrupt:
	communication.stopReadingInput()
	communication.stopProbResetId()


