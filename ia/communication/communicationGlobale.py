# -*- coding: utf-8 -*-
"""
Ce fichier est objet qui gère toute la communication
"""

from collections import deque
import time

from . import parser_c
from . import serial_comm
from . import conversion
import threading


class communicationGlobale():
	def __init__(self, port):
		#on récupère les constantes
		self.address = {}
		self.orders = {}
		self.ordersArguments = {}
		self.ordersRetour = {}
		self.ordersSize = {}
		(self.address, self.orders, self.ordersSize, self.ordersArguments, self.ordersRetour) = parser_c.parseConstante()
		self.ordreLog = [[(-1,"")]*64 for x in range(len(self.address)//2+1)] #stock un historique des ordres envoyés, double tableau de tuple (ordre,data)

		for order in self.orders:
			self.checkParsedOrderSize(order)
		
		self.arduinoIdReady = [False]*(len(self.address)//2+1)
		self.lastConfirmationDate = [-1]*(len(self.address)//2+1)#date de la dernière confirmation(en milliseconde)
		self.lastSendDate = [-1]*(len(self.address)//2+1)#date du dernier envoie(en milliseconde)
		self.lastIdConfirm = [63]*(len(self.address)//2+1)
		self.lastIdSend = [63]*(len(self.address)//2+1)
		self.nbUnconfirmedPacket = [(0, -1)]*(len(self.address)//2+1) # (nbUnconfimed, dateFirstUnconfirmed)

		self.liaisonXbee = serial_comm.ComSerial(port, 57600)


		#defines de threads
		self.lastHighPrioTaskDate = 0
		self.highPrioSpeed = 10 #fréquence d'execution en ms
		self.lastLowPrioTaskDate = 0
		self.lowPrioSpeed = 1000
		self.maxUnconfirmedPacket = 5 # attention maximum 32

		self.threadActif = True
		self.writeOutput = True
		self.readInput = True
		self.probingDevices = True
		self.renvoieOrdre = True
		self.keepContact = True

		self.ordersToRead = deque()
		self.ordersToSend = deque()
		self.mutexOrdersToRead = threading.Lock()
		self.mutexOrdersToSend = threading.Lock()
		gestionThread = threading.Thread(target=self.gestion)
		gestionThread.start()
		


	def getConst(self):
		return (self.address, self.orders, self.ordersSize, self.ordersArguments, self.ordersRetour)

		
			

						#Thread

	def gestion(self):
		while self.threadActif:
			date = int(time.time()*1000)
			
			#tâches de hautes priotités
			if (date - self.lastHighPrioTaskDate) > self.highPrioSpeed:
				self.lastHighPrioTaskDate = date

				#Ecriture des ordres
				if self.writeOutput == True:
					self.sendOrders()

				#Lecture des entrées
				if self.readInput == True:
					self.mutexOrdersToRead.acquire()
					self.ordersToRead += self.readOrders()
					self.mutexOrdersToRead.release()

				#Renvoie des ordres non confirmés
				if self.renvoieOrdre == True:
					for address in self.address:
						if isinstance(address, (int)):
							if (date - self.nbUnconfirmedPacket[address][1] > 40) and(self.nbUnconfirmedPacket[address][1] != -1):#si il reste un ordre non confirmé en moins de X ms
								self.nbUnconfirmedPacket[address] = (self.nbUnconfirmedPacket[address][0], date)
								indiceARenvoyer = self.getAllUnknowledgeId(address)
								for indice in indiceARenvoyer:
									print(("WARNING: Renvoie de l'ordre: ", self.orders[self.ordreLog[address][indice][0]], "d'idd ", indice, "au robot ", self.address[address]), "binaire :", self.ordreLog[address][indice])
									self.liaisonXbee.send(self.ordreLog[address][indice][1])
									self.lastSendDate[address] = date 

			#tâche de faibles priorités
			if (date - self.lastLowPrioTaskDate) > self.lowPrioSpeed:
				self.lastLowPrioTaskDate = date
				#recherche d'arduino
				if self.probingDevices == True:
					for address in range(1, len(self.address)//2+1, 1):
						if self.arduinoIdReady[address] == False:
							self.askResetId(address)

				#Verification de la liaison avec les arduinos
				if self.keepContact == True:# On envoie un PING pour verifier si le device est toujours présent
					for address in self.address:
						if isinstance(address, (int)):
							if self.arduinoIdReady[address]:
								if ((date - self.lastConfirmationDate[address]) > 5000) and self.lastConfirmationDate[address] != -1:#le système est considere comme hors ligne
									self.arduinoIdReady[address] = False
								elif (date - self.lastSendDate[address]) > 1000:
									self.sendOrderAPI(address, self.orders['PINGPING_AUTO'])

			waitBeforeNextExec = (self.highPrioSpeed -(int(time.time()*1000) - date))
			if waitBeforeNextExec < 1:
				print(("Warning: La boucle de pool de communication n'est pas assez rapide ", waitBeforeNextExec))
			else:
				time.sleep(waitBeforeNextExec/1000.0)


	def stopGestion(self):
		self.threadActif = False









						#Gestion des id

	def getId(self, address):
		"""retourne l'id qu'il faut utiliser pour envoyer un packet à l'adresse passé en argument"""
		if self.lastIdSend[address] == 63:
			self.lastIdSend[address] = 0
		else:
			self.lastIdSend[address] += 1

		return self.lastIdSend[address]

	def getNextConfirmeId(self, address):
		"""retourne le prochain id attendu"""
		if self.lastIdConfirm[address] == 63:
			return 0
		else:
			return self.lastIdConfirm[address]+1

	def getAllUnknowledgeId(self, address):
		if self.lastIdSend[address] != self.lastIdConfirm[address]:
			unconfirmedId = self.getNextConfirmeId(address)
			unconfirmedIds = (unconfirmedId,)
			while unconfirmedId != self.lastIdSend[address]:
				if unconfirmedId == 63:
					unconfirmedId = 0
				else:
					unconfirmedId +=1
				unconfirmedIds += (unconfirmedId,)
			return unconfirmedIds
		return ()

	def incrementeLastConfirmedId(self, address):
		if self.lastIdConfirm[address] == 63:
			self.lastIdConfirm[address] = 0
		else:
			self.lastIdConfirm[address] += 1


	def removeOrdersInFile(self, address):# Warning, only on reset !
		remainOrdersToSend = deque()
		self.mutexOrdersToSend.acquire()
		for packet in self.ordersToSend:
			if packet[0] != address:
				remainOrdersToSend.append(packet)
			else:
				print(("ERREUR: drop de l'ordre", packet[1], " par l'arduino", packet[0], "suite à un reset"))
		self.ordersToSend = remainOrdersToSend
		self.mutexOrdersToSend.release()

	def askResetId(self, address): #demande a une arduino de reset
		self.removeOrdersInFile(address)
		self.lastConfirmationDate[address] = -1
		self.nbUnconfirmedPacket[address] = (0, -1)
		self.lastSendDate[address] = -1
		self.arduinoIdReady[address] = False
		self.lastIdConfirm[address] = 63
		self.lastIdSend[address] = 63

		chaineTemp = chr(address+192)
		self.liaisonXbee.send(chaineTemp)


	#cas où on reçoi
	def acceptConfirmeResetId(self, address):#accepte la confirmation de reset d'un arduino
		print(("L'arduino "+ str(address)+" a accepte le reset"))
		self.removeOrdersInFile(address)
		self.lastConfirmationDate[address] = -1
		self.nbUnconfirmedPacket[address] = (0, -1)
		self.lastSendDate[address] = -1
		self.arduinoIdReady[address] = True
		self.lastIdConfirm[address] = 63
		self.lastIdSend[address] = 63
		

	def confirmeResetId(self, address):#renvoie une confirmation de reset
		print(("Reponse au reset de l'arduino "+ str(address)))
		self.removeOrdersInFile(address)
		self.lastConfirmationDate[address] = -1
		self.nbUnconfirmedPacket[address] = (0, -1)
		self.lastSendDate[address] = -1
		self.arduinoIdReady[address] = True
		self.lastIdConfirm[address] = 63
		self.lastIdSend[address] = 63

		chaineTemp = chr(address+224)
		self.liaisonXbee.send(chaineTemp)







	def extractData(self, rawInput):
		""" prend rawInput une chaine de caractère qui correspond  qui correspond à un ordre, retourne les autres packerData est prêt à être interpréter"""
		
		"""print "DEBUG"
		for letter in rawInput:
			print conversion.intToBinary(ord(letter))
		print "FIN DEBUG"""

		if len(rawInput) >0:#cas improbable, mais il semble que ça arrive

			packetAddress = ord(rawInput[0]) - 128

			if packetAddress > 96:# l'arduino confirme le reset
				if packetAddress-96 in self.address:
					self.acceptConfirmeResetId(packetAddress-96)
				else:
					print("WARNING, corrupted address on reset confirme from arduino")
				return 0

			elif packetAddress > 64:# l'arduino demande un reset
				if packetAddress-64 in self.address:
					self.confirmeResetId(packetAddress-64)
				else:
					print("WARNING, corrupted address on reset confirme from arduino")
				return 0

			elif len(rawInput)>=3:#cas normal
				packetId = ord(rawInput[1])
				rawInput = rawInput[2:-1] # on supprime les deux carctères du dessus et le paquet de fin
				
				#python enleve les zero lors de la conversion en binaire donc on les rajoute, sauf le premier du protocole
				packetData = ""
				for octet in rawInput:
					temp = bin(ord(octet))[2:]
					while len(temp) < 7:
						temp = '0' + temp
					packetData += temp

				if (packetAddress in self.address) and packetId >= 0 and packetId < 64:
					taille = 0
					for returnType in self.ordersRetour[self.orders[ self.ordreLog[packetAddress][packetId][0] ]]:
						if returnType == 'int':
							taille += 2
						elif returnType == 'float':
							taille += 4
						elif returnType == 'long':
							taille += 4
						else:
							print("ERREUR: Parseur: le parseur a trouvé un type non supporté")

					if len(packetData)//8 == taille:# si la longeur des données reçu est bonne
						return (packetAddress, packetId, packetData)
					else:
						print(("WARNING: Le paquet ne fait pas la bonne taille, des données ont probablement été perdue, paquet droppé, taille attendu ", taille))
						return 0
				elif packetId > 63:
					print(("L'arduino", self.address[packetAddress], "nous indique avoir mal reçu un message, message d'erreur ", packetId))
					return 0
				else:
					print("WARNING: Le paquet est mal formé, l'address ou l'id est invalide")
					return 0
			else:
				print("WARNING: Le paquet ne fait même pas 3 octet, des données ont probablement été perdue, paquet droppé")
				return 0
		else:
			print("WARNING: Le paquet ne fait même pas 1 octet, des données ont probablement été perdue, paquet droppé")
			return 0
		print("Erreur: erreur de code, cas non gérer")
		return 0# ne doit pas arriver

	def getXbeeOrders(self):
		""" retourne ordersList, une liste d'élements sous la forme(adresse, id, data) où data est prêt à être interpréter"""
		rawInputList = self.liaisonXbee.read()

		ordersList = deque()

		for rawInput in rawInputList:
			ret = self.extractData(rawInput)
			if ret != 0 and ret != None:# cas où les données sont de la bonne taille et que ça n'a rien à voir avec le système de reset
				ordersList.append(ret)

		return ordersList


	def readOrders(self):
		ordersList = self.getXbeeOrders()

		returnOrders = deque()

		for order in ordersList:
			address = int(order[0])
			idd = int(order[1])
			arguments = []

			if address in self.address:
				if idd >= 64:# cas impossible car verification lors de l'extraction des données
					print(("ERREUR: IMPOSSIBLE l'arduino", self.address[address], " a mal recu un message."))
				else:
					if idd in self.getAllUnknowledgeId(address):
						if self.ordreLog[address][idd][0] != self.orders['PINGPING_AUTO']:
							print(("Success: l'arduino", self.address[address]," a bien recu l'ordre ", self.orders[self.ordreLog[address][idd][0]], " d'id: ", idd))
						date = int(time.time()*1000)
						self.nbUnconfirmedPacket[address] = (self.nbUnconfirmedPacket[address][0] - self.getAllUnknowledgeId(address).index(idd) - 1, date)#on bidone le chiffre date, mais c'est pas grave
						self.lastIdConfirm[address] = idd
						self.lastConfirmationDate[address] = date
						
						index = 0
						for returnType in self.ordersRetour[self.ordreLog[address][idd][0]]:
							if returnType == 'int':
								retour = conversion.binaryToInt(order[2][index*8:(index+2)*8])
								print(("Retour int: ", retour))
								arguments.append(retour)
								index += 2
							elif returnType == 'float':
								retour = conversion.binaryToFloat(order[2][index*8:(index+4)*8])
								print(("Retour float: ", retour))
								arguments.append(retour)
								index += 4
							elif returnType == 'long':
								retour = conversion.binaryToLong(order[2][index*8:(index+4)*8])
								print(("Retour long: ", retour))
								arguments.append(retour)
								index += 4
							else:
								print("ERREUR: Parseur: le parseur a trouvé un type non supporté")

						returnOrders.append((address, idd, arguments))
						arguments = []

					else:
						print("WARNING: l'arduino", self.address[address], "a accepte le paquet", idd, "alors que les paquets a confirmer sont ", self.getAllUnknowledgeId(address))
			else:
				print("ERREUR: address: ", address, " inconnue")
			
		return returnOrders



	#Envoi
	def sendXbeeOrder(self, address, idd, order, chaineTemp):
		self.ordreLog[address][idd] = (order, chaineTemp)
		date = int(time.time()*1000)
		self.lastSendDate[address] = date
		self.liaisonXbee.send(chaineTemp)

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

		return (chaineRetour)

	def sendOrders(self):
		"""fonction qui gère l'envoi des ordres, sous le contrôle du thread"""

		remainOrdersToSend = deque()
		self.mutexOrdersToSend.acquire()
		for packet in self.ordersToSend:#packet contient(address, ordre, *argument)
			#si il n'y a pas déjà trop d'ordres en atente on envoie
			if self.nbUnconfirmedPacket[packet[0]][0] < self.maxUnconfirmedPacket:
				self.nbUnconfirmedPacket[packet[0]] = (self.nbUnconfirmedPacket[packet[0]][0]+1, int(time.time()*1000)) # on s'occupe de [1] dans sendXbeeOrder
				data = conversion.orderToBinary(packet[1])
				i = 0

				for typeToGet in self.ordersArguments[packet[1]]:
					if typeToGet == 'int':
						data += conversion.intToBinary(int(packet[2][i]))
					elif typeToGet == 'long':
						data += conversion.longToBinary(int(packet[2][i]))
					elif typeToGet == 'float':
						data += conversion.floatToBinary(float(packet[2][i]))
					else:
						print("ERREUR: Parseur: le parseur a trouvé un type non supporté")
					i += 1
				idd = self.getId(packet[0])
				chaineTemp = self.applyProtocole(packet[0], idd, data)
				self.sendXbeeOrder(packet[0], idd, packet[1], chaineTemp)
			else:
				remainOrdersToSend.append(packet)

		self.ordersToSend = remainOrdersToSend
		self.mutexOrdersToSend.release()







						#fonctions de verifications diverses
	def checkAddress(self, address):
		"""verifie que l'address existe et la convertie en int si nécéssaire, sinon retourne -1"""
		if address in self.address:
			if isinstance(address, (str)):
				address = self.address[address]
			return address
		else:
			print(("ERREUR COMM: L'address: ", address, " est invalide."))
			return -1

	def checkOrder(self, order):
		"""verifie l'ordre et le convertie en int si nécessaire, sinon retourne -1"""
		if order in self.orders:
			if isinstance(order, (str)):
				order = self.orders[order]
			return order
		else:
			print(("ERREUR COMM: L'ordre: ", order, " est invalide."))
			return -1

	def checkParsedOrderSize(self, order):
		"""check parsed sizes"""
		if isinstance(order, (int)):
			order = self.orders[order]

		if order in self.ordersSize:#verification
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
				print(("ERREUR: la constante de taille de l'ordre ", order, " ne correspond pas aux types indiqués attendu ", sizeExpected, " calculee ", somme))
		else:
			print(("ERREUR l'ordre ", order, "n'a pas été trouvé dans serial_defines.c"))

	def checkOrderArgument(self, order, *arguments):
		"""check a given set of argument for an order, if all arguments type match return 0 else return -1"""
		#orderSize need str argument
		if isinstance(order, (int)):
			order = self.orders[order]

		if len(arguments) == len(self.ordersArguments[order]):
			for i, argumentType in enumerate(self.ordersArguments[order]):
				if argumentType == 'int':
					if not isinstance(arguments[i], (int)):
						print(("L'argument ", i, " de l'ordre ", order, " n'est pas du bon type, attendu (int)"))
						return -1
				elif argumentType == 'long':
					if not isinstance(arguments[i], (int)):
						print(("L'argument ", i, " de l'ordre ", order, " n'est pas du bon type, attendu (long)"))
						return -1
				elif argumentType == 'float':
					if not isinstance(arguments[i], (float)):
						print(("L'argument ", i, " de l'ordre ", order, " n'est pas du bon type, attendu (float)"))
						return -1
				else:
					print("ERREUR: attendu type inconnu")
					
		else:
			print(("ERREUR: l'order", order, "attend", len(self.ordersArguments[order]), "arguments, mais a recu:", len(arguments), "arguemnts"))
			return -1

		return 0





	def sendOrderAPI(self, address, order, *arguments):
		""""api d'envoie d'ordres avec verification des parametres, retourne False en cas d'erreur"""
		#on verifie l'address
		address = self.checkAddress(address)
		order = self.checkOrder(order)

		if address !=-1 and order !=-1 and self.checkOrderArgument(order, *arguments) !=-1:
			self.mutexOrdersToSend.acquire()
			self.ordersToSend.append((address, order, arguments))
			self.mutexOrdersToSend.release()
			return 0
		else:
			return -1
		


	def readOrdersAPI(self):
		"""Renvoi -1 si pas d'ordre en attente sinon renvoi un ordre """
		self.mutexOrdersToRead.acquire()
		if len(self.ordersToRead) > 0:
			order = self.ordersToRead.pop()
			self.mutexOrdersToRead.release()
			return order
		else:
			self.mutexOrdersToRead.release()
			return -1
