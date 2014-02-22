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
	def __init__(self, portXbee, vitesseXbee, parityXbee, portOther, vitesseOther, parityOther, portAsserv, vitesseAsserv, parityAsserv):
		self.nbTimeoutPaquets=0
		self.nbTransmitedPaquets = 0

		#Constantes réglables:
		self.useXbee = True
		self.useFMother = False
		self.useFMasserv = False
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
		self.renvoiImmediat = False



		#on récupère les constantes
		self.address = {}
		self.orders = {}
		self.ordersArguments = {}
		self.ordersRetour = {}
		self.argumentSize = {}
		self.returnSize = {}
		(self.address, self.orders, self.argumentSize, self.ordersArguments, self.ordersRetour) = parser_c.parseConstante()
		self.nbAddress = len(self.address)//2


		for order in self.orders:#revertion de self.argumentSize
			if isinstance(order, (str)):
				size = self.argumentSize[order]
				self.argumentSize[self.orders[order]] = size

		#on crée un dico de taille de retour
		for order in self.orders:
			size = 0
			for i,typeToGet in enumerate(self.ordersRetour[order]):
				if typeToGet == 'int':
					size += 2
				elif typeToGet == 'long':
					size += 4				
				elif typeToGet == 'float':
					size += 4
				else:
					print("ERREUR: Parseur: le parseur a trouvé un type non supporté")
			self.returnSize[order] = size

		for order in self.orders:# on vérifie la cohérance entre serial_defines.c et serial_defines.h
			self.checkParsedOrderSize(order)
		
		self.ordreLog = [[(-1,"")]*64 for x in range(self.nbAddress+1)] #stock un historique des ordres envoyés, double tableau de tuple (ordre,data)
		self.arduinoIdReady = [False]*(self.nbAddress+1)
		self.lastConfirmationDate = [-1]*(self.nbAddress+1)#date de la dernière confirmation(en milliseconde)
		self.lastSendDate = [-1]*(self.nbAddress+1)#date du dernier envoie(en milliseconde)
		self.lastIdConfirm = [63]*(self.nbAddress+1)
		self.lastIdSend = [63]*(self.nbAddress+1)
		self.nbRenvoiImmediat = [0]*(self.nbAddress+1)
		self.nbNextRenvoiImmediat = [0]*(self.nbAddress+1)
		self.nbUnconfirmedPacket = [(0, -1)]*(self.nbAddress+1) # (nbUnconfimed, dateFirstUnconfirmed)
		
		
		if self.useXbee:
			self.liaisonXbee = serial_comm.ComSerial(portXbee, vitesseXbee, parityXbee)
		if self.useFMother:
			self.liaisonArduinoOther = serial_comm.ComSerial(portOther, vitesseOther, parityOther)
		if self.useFMasserv:
			self.liaisonArduinoAsserv = serial_comm.ComSerial(portAsserv, vitesseAsserv, parityAsserv)

		#defines de threads
		self.lastHighPrioTaskDate = 0
		self.lastLowPrioTaskDate = 0

		self.ordersToRead = deque()
		self.ordersToSend = deque()
		self.mutexOrdersToRead = threading.Lock()
		self.mutexOrdersToSend = threading.Lock()
		gestionThread = threading.Thread(target=self.gestion)
		gestionThread.start()
		


	def getConst(self):
		return (self.address, self.orders, self.argumentSize, self.ordersArguments, self.ordersRetour)

		
			

						#Thread

	def gestion(self):
		while self.threadActif:
			date = int(time.time()*1000)
			
			#tâches de hautes priotités
			if (date - self.lastHighPrioTaskDate) > self.highPrioSpeed:
				self.lastHighPrioTaskDate = date

				#Lecture des entrées
				if self.readInput == True:
					self.mutexOrdersToRead.acquire()
					self.ordersToRead += self.readOrders()
					self.mutexOrdersToRead.release()

				#Renvoie des ordres non confirmés
				if self.renvoiOrdre == True:
					for address in self.address:
						if isinstance(address, (int)):
							indiceARenvoyer = self.getAllUnknowledgeId(address)
							if len(indiceARenvoyer) > 0:

								#procedure de renvoi immediat dans le cas où l'arduino indique une erreur
								if self.renvoiImmediat == True:
									if self.nbRenvoiImmediat[address] != 0:
										for i in range(self.nbRenvoiImmediat[address]):
											if i < len(indiceARenvoyer):
												print("WARNING: Renvoie immediat de l'ordre: ", self.orders[self.ordreLog[address][indiceARenvoyer[i]][0]], "d'idd ", indiceARenvoyer[i], "au robot ", self.address[address])
												self.sendMessage(address, self.ordreLog[address][indiceARenvoyer[i]][1])
												self.lastSendDate[address] = date 
												self.nbUnconfirmedPacket[address] = (self.nbUnconfirmedPacket[address][0], date)
												self.lastIdSend[address] = i
											else:
												print("ERREUR CODE: cas impossible")
												print(indiceARenvoyer)
												print(self.nbRenvoiImmediat[address])
										self.nbNextRenvoiImmediat[address] = len(indiceARenvoyer) - self.nbRenvoiImmediat[address]
										self.nbRenvoiImmediat[address] = 0

								#procedure de renvoi en cas de timeout
								if (date - self.nbUnconfirmedPacket[address][1]) > self.timeOut and self.nbUnconfirmedPacket[address][1] != -1:
									for indice in indiceARenvoyer:
										self.nbTimeoutPaquets += 1
										print("WARNING: Renvoie après timeout de l'ordre: ", self.orders[self.ordreLog[address][indice][0]], "d'idd ", indice, "au robot ", self.address[address], "binaire :", self.ordreLog[address][indice])
										self.sendMessage(address, self.ordreLog[address][indice][1])
										self.lastSendDate[address] = date 
										self.nbUnconfirmedPacket[address] = (self.nbUnconfirmedPacket[address][0], date)
										self.lastIdSend[address] = indice
				#Ecriture des ordres
				if self.writeOutput == True:
					self.sendOrders()
									
			#tâche de faibles priorités
			if (date - self.lastLowPrioTaskDate) > self.lowPrioSpeed:
				self.lastLowPrioTaskDate = date

				#recherche d'arduino
				if self.probingDevices == True:
					for address in self.address:
						if isinstance(address, (int)):
							if self.arduinoIdReady[address] == False:
								self.askResetId(address)

				#Verification de la liaison avec les arduinos
				if self.keepContact == True:# On envoie un PING pour verifier si le device est toujours présent
					for address in self.address:
						if isinstance(address, (int)):
							if self.arduinoIdReady[address] != False:
								if (date - self.lastConfirmationDate[address]) > self.offLigneTimeout and (date - self.arduinoIdReady[address]) > self.offLigneTimeout:#le système est considere comme hors ligne
									print("L'arduino", self.address[address], "va être reset car elle a depasser le timeout")
									self.arduinoIdReady[address] = False
								elif (date - self.lastSendDate[address]) > self.keepContactTimeout:
									self.sendOrderAPI(address, self.orders['PINGPING_AUTO'])

			waitBeforeNextExec = (self.highPrioSpeed -(int(time.time()*1000) - date))
			if waitBeforeNextExec < 1:
				print("Warning: La boucle de pool de communication n'est pas assez rapide ", waitBeforeNextExec)
			else:
				time.sleep(waitBeforeNextExec/1000.0)


	def stopGestion(self):
		self.threadActif = False


	def sendMessage(self, address, data):
		if address == self.address['ADDR_FLUSSMITTEL_OTHER'] and self.useFMother: 
			self.liaisonArduinoOther.send(data)
		elif address == self.address['ADDR_FLUSSMITTEL_ASSERV'] and self.useFMasserv:
			self.liaisonArduinoAsserv.send(data)
		elif self.useXbee:
			self.liaisonXbee.send(data)







						#Gestion des id

	def getId(self, address):
		"""retourne l'id qu'il faut utiliser pour envoyer un packet à l'adresse passé en argument"""
		if self.lastIdSend[address] == 63:
			self.lastIdSend[address] = 0
		else:
			self.lastIdSend[address] += 1

		return self.lastIdSend[address]

	def getNextIdOfId(self, idd):
		"""retourne l'id d'après"""
		if idd != 63:
			return idd+1
		else:
			return 0

	def getNextConfirmeId(self, address):
		"""retourne le prochain id attendu"""
		if self.lastIdConfirm[address] != 63:
			return self.lastIdConfirm[address]+1
		else:
			return 0

	def getAllUnknowledgeId(self, address):
		if self.lastIdSend[address] != self.lastIdConfirm[address]:
			unconfirmedId = self.getNextConfirmeId(address)
			unconfirmedIds = (unconfirmedId,)
			while unconfirmedId != self.lastIdSend[address]:
				if unconfirmedId != 63:
					unconfirmedId += 1
				else:
					unconfirmedId = 0
				unconfirmedIds += (unconfirmedId,)
			return unconfirmedIds
		return ()


	def removeOrdersInFile(self, address):# Warning, only on reset !
		remainOrdersToSend = deque()
		self.mutexOrdersToSend.acquire()
		for packet in self.ordersToSend:
			if packet[0] != address:
				remainOrdersToSend.append(packet)
			else:
				print("ERREUR: drop de l'ordre",self.orders[ packet[1]], " par l'arduino", self.address[ packet[0]], "suite à un reset")
		self.ordersToSend = remainOrdersToSend
		self.mutexOrdersToSend.release()

	def askResetId(self, address): #demande a une arduino de reset
		self.removeOrdersInFile(address)
		self.lastConfirmationDate[address] = -1
		self.nbUnconfirmedPacket[address] = (0, -1)
		self.lastSendDate[address] = -1
		self.arduinoIdReady[address] = False
		self.nbRenvoiImmediat[address] = 0
		self.nbNextRenvoiImmediat[address] = 0
		self.lastIdConfirm[address] = 63
		self.lastIdSend[address] = 63

		chaineTemp = chr(address+192)
		self.sendMessage(address, chaineTemp)


	#cas où on reçoi
	def acceptConfirmeResetId(self, address):#accepte la confirmation de reset d'un arduino
		print("L'arduino ", self.address[address], " a accepte le reset")
		self.removeOrdersInFile(address)
		self.lastConfirmationDate[address] = -1
		self.nbUnconfirmedPacket[address] = (0, -1)
		self.lastSendDate[address] = -1
		self.arduinoIdReady[address] = int(time.time()*1000)
		self.nbRenvoiImmediat[address] = 0
		self.nbNextRenvoiImmediat[address] = 0
		self.lastIdConfirm[address] = 63
		self.lastIdSend[address] = 63
		

	def confirmeResetId(self, address):#renvoie une confirmation de reset
		print("Reponse à la demande de confirmation de reset de l'arduino ", self.address[address])
		self.removeOrdersInFile(address)
		self.lastConfirmationDate[address] = -1
		self.nbUnconfirmedPacket[address] = (0, -1)
		self.lastSendDate[address] = -1
		self.arduinoIdReady[address] = int(time.time()*1000)
		self.nbRenvoiImmediat[address] = 0
		self.nbNextRenvoiImmediat[address] = 0
		self.lastIdConfirm[address] = 63
		self.lastIdSend[address] = 63

		chaineTemp = chr(address+224)
		self.sendMessage(address, chaineTemp)







	def extractData(self, rawInput):
		""" prend rawInput une chaine de caractère qui correspond  qui correspond à un ordre, retourne les autres packerData est prêt à être interpréter"""
		
		"""print("DEBUG")
		for letter in rawInput:
			print(conversion.intToBinary(letter)[:8])
		print("FIN DEBUG")"""

	

		packetAddress = rawInput[0] - 128

		if packetAddress > 96:# l'arduino confirme le reset
			if packetAddress-96 in self.address:
				self.acceptConfirmeResetId(packetAddress-96)
				return 0
			else:
				print("WARNING, corrupted address on reset confirme from arduino, adress", packetAddress-96)
				return -1

		elif packetAddress > 64:# l'arduino demande un reset
			if packetAddress-64 in self.address:
				self.confirmeResetId(packetAddress-64)
				return 0
			else:
				print("WARNING, corrupted address on reset request from arduino, address", packetAddress-64)
				return -1

		elif len(rawInput)>=3:#cas normal
			packetId = rawInput[1]

			# si la longeur des données reçu est bonne
			if packetAddress > 0 and packetAddress < (self.nbAddress+1) and packetId >= 0 and packetId < 64:
				order = self.ordreLog[packetAddress][packetId][0]
				if order != -1:
					if len(rawInput[2:-1])*7//8 == self.returnSize[ order ]:
						return (packetAddress, packetId, rawInput[2:-1])# on supprime les deux carctères du dessus et le paquet de fin
					else:
						print("WARNING: Le paquet est mal formé, l'address ou l'id est invalide debug_A")
						return -1
				else:
					print("On essaye de lire, l'id", packetId, "en provenance de l'arduino", self.address[packetAddress], "mais il n'est existe pas de trace dans le log (un vieux paquet qui trainait sur un client avant la nouvelle init ?)")
					return -1
			elif packetAddress > 0 and packetAddress < (self.nbAddress+1) and packetId > 63:
				print("L'arduino", self.address[packetAddress], "nous indique avoir mal reçu un message, message d'erreur ", packetId)
				if self.nbNextRenvoiImmediat[packetAddress] != 0:
					self.nbRenvoiImmediat[packetAddress] += 1
				return -1
			else:
				print("WARNING: Le paquet est mal formé, l'address ou l'id est invalide")
				return -1
		else:
			print("WARNING: Le paquet n'est pas un reset et ne fait même pas 3 octet, des données ont probablement été perdue, paquet droppé")
			return -1

	def getXbeeOrders(self):
		rawInputList = []
		""" retourne ordersList, une liste d'élements sous la forme(adresse, id, data) où data est prêt à être interpréter"""
		if self.useXbee:
			rawInputList += self.liaisonXbee.read()
		if self.useFMother:
			rawInputList += self.liaisonArduinoOther.read()
		if self.useFMasserv:
			rawInputList += self.liaisonArduinoAsserv.read()

		ordersList = deque()

		for rawInput in rawInputList:
			ret = self.extractData(rawInput)
			if ret != -1 and ret != 0 and ret != None:# cas où les données sont de la bonne taille et que ça n'a rien à voir avec le système de reset
				ordersList.append(ret)

		return ordersList


	def readOrders(self):
		ordersList = self.getXbeeOrders()
		returnOrders = deque()

		for order in ordersList:
			address = int(order[0])
			idd = int(order[1])
			
			unconfirmedIds = self.getAllUnknowledgeId(address)
			if idd in unconfirmedIds:
				#ne pas renvoyer  les paquets sans argument et dont on a louppé les confimations
				date = int(time.time()*1000)
				returnMissed = False
				lastIdToAccept = -1

				if idd == self.getNextConfirmeId(address):
					if self.ordreLog[address][idd][0] != self.orders['PINGPING_AUTO']:
						print("Success: l'arduino", self.address[address]," a bien recu l'ordre ", self.orders[self.ordreLog[address][idd][0]], " d'id: ", idd)
					self.nbTransmitedPaquets +=1
					self.nbUnconfirmedPacket[address] = (self.nbUnconfirmedPacket[address][0] - unconfirmedIds.index(idd) - 1, date)#on bidone le chiffre date, mais c'est pas grave
					self.lastIdConfirm[address] = idd
					self.lastConfirmationDate[address] = date
				else:
					i = 0
					lastIdToAccept = self.lastIdConfirm[address]
					while lastIdToAccept != idd and returnMissed == False:
						if (self.returnSize[ self.ordreLog[address][unconfirmedIds[i]][0] ] == 0 and returnMissed == False):
							lastIdToAccept = unconfirmedIds[i]
						else:
							returnMissed = True
						if i > self.maxUnconfirmedPacket:
							print("ERREUR CODE: ce cas ne devrait pas arriver")
						i +=1

					if lastIdToAccept != self.lastIdConfirm[address]:
						if returnMissed == True:
							print("Success: l'arduino", self.address[address]," a bien recu les ordres jusque", idd, "mais il manque au moins un retour (avec argument) donc on ne confirme que", self.orders[self.ordreLog[address][lastIdToAccept][0]], " d'id: ", lastIdToAccept)
							self.nbTransmitedPaquets += 1
							self.nbUnconfirmedPacket[address] = (self.nbUnconfirmedPacket[address][0] - unconfirmedIds.index(lastIdToAccept) - 1, date)#on bidone le chiffre date, mais c'est pas grave
							self.lastIdConfirm[address] = lastIdToAccept
						
					
					self.lastConfirmationDate[address] = date
					
				if idd == self.getNextConfirmeId(address) or lastIdToAccept != self.lastIdConfirm[address]:
					#python enleve les zero lors de la conversion en binaire donc on les rajoute, sauf le premier du protocole
					argumentData = ""
					for octet in order[2]:
						temp = bin(octet)[2:].zfill(7)
						argumentData += temp

					arguments = []
					index = 0
					for returnType in self.ordersRetour[self.ordreLog[address][idd][0]]:
						if returnType == 'int':
							size = 16
							retour = conversion.binaryToInt(argumentData[index:index+size])
							arguments.append(retour)
							index += size
						elif returnType == 'float':
							size = 32
							retour = conversion.binaryToFloat(argumentData[index:index+size])
							arguments.append(retour)
							index += size
						elif returnType == 'long':
							size = 32
							retour = conversion.binaryToInt(argumentData[index:index+size])
							arguments.append(retour)
							index += size
						else:
							print("ERREUR: Parseur: le parseur a trouvé un type non supporté")

					returnOrders.append((address, self.ordreLog[address][idd][0], arguments))

					if len(arguments) > 0:
						print("Retour :", arguments)

			else:
				print("WARNING: l'arduino", self.address[address], "a accepte le paquet", idd, "alors que les paquets a confirmer sont ", self.getAllUnknowledgeId(address), " sauf si on a louppé une réponse avec arguments")
			
		return returnOrders



	def applyProtocole(self, address, idd, order, data):
		""" on concatène les trois parametres et on retourne chaineRetour en appliquant le protocole """
		rawBinary = conversion.orderToBinary(order)
		for i,typeToGet in enumerate(self.ordersArguments[order]):
			if typeToGet == 'int':
				rawBinary += conversion.intToBinary(data[i])
			elif typeToGet == 'long':
				rawBinary += conversion.intToBinary(data[i])
			elif typeToGet == 'float':
				rawBinary += conversion.floatToBinary(data[i])
			else:
				print("ERREUR: Parseur: le parseur serial_defines a trouvé un type non supporté")
		
		while len(rawBinary)%7 != 0: # hack pour former correctement le dernier octet
			rawBinary += '0'
		
		chaineRetour = ""
		chaineRetour += chr(address + 128)
		chaineRetour += chr(idd)
		for i in range(0, len(rawBinary), 7):
			chaineRetour += chr(int(rawBinary[i:i+7], 2))

		#on ajoute l'octet de fin
		chaineRetour += chr(128)

		return (chaineRetour)

	def sendOrders(self):
		"""fonction qui gère l'envoi des ordres, sous le contrôle du thread"""
		date = int(time.time()*1000)

		#gestion du cas particulier où l'arduino a perdue un paquet, en effet il faut d'abbord lui renvoyer les autres paquets perdue avant d'en envoyer des nouveau
		for address in self.address:
			if isinstance(address, (int)):
				while self.nbNextRenvoiImmediat[address] > 0 and self.nbUnconfirmedPacket[address][0] < self.maxUnconfirmedPacket:
					print("Warning: procédure de renvoi après un renvoi immediat sur l'arduino", self.address[address], "du paquets d'id", self.getNextIdOfId(self.lastIdSend[address]))
					self.sendMessage(address, self.ordreLog[address][self.getNextIdOfId(self.lastIdSend[address])][1])
					self.nbNextRenvoiImmediat[address] -= 1
					self.lastSendDate[address] = date
					self.lastIdSend[address] = self.getNextIdOfId(self.lastIdSend[address])
					self.nbUnconfirmedPacket[address] = (self.nbUnconfirmedPacket[address][0], date)

		#cas d'envoi normal
		remainOrdersToSend = deque()
		self.mutexOrdersToSend.acquire()
		for packet in self.ordersToSend:#packet contient(address, ordre, *argument)
			#si il n'y a pas déjà trop d'ordres en atente on envoi
			if self.nbUnconfirmedPacket[packet[0]][0] < self.maxUnconfirmedPacket:
				address = packet[0]
				order = packet[1]
				self.nbUnconfirmedPacket[address] = (self.nbUnconfirmedPacket[address][0]+1, date)
				
				idd = self.getId(address)
				chaineTemp = self.applyProtocole(address, idd, order, packet[2])

				self.ordreLog[int(address)][idd] = (order, chaineTemp)
				self.lastSendDate[address] = date
				self.lastIdSend[address] = idd
				#print("Envoi normal a l'arduino", self.address[address], "de l'ordre", self.orders[order], "d'id", idd)
				self.sendMessage(address, chaineTemp)
			else:
				remainOrdersToSend.append(packet)

		self.ordersToSend = remainOrdersToSend
		self.mutexOrdersToSend.release()

		if len(remainOrdersToSend) == 0 and not self.emptyFifo:
			self.emptyFifo = True
			print("Fin de transmission de la file, (t = "+str(int(time.time()*1000)-self.timeStartProcessing)+"ms),nombre de paquets reçu", self.nbTransmitedPaquets," nombre de paquets perdu", self.nbTimeoutPaquets)
		







						#fonctions de verifications diverses
	def checkAddress(self, address):
		"""verifie que l'address existe et la convertie en int si nécéssaire, sinon retourne -1"""
		if address in self.address:
			if self.arduinoIdReady[address] != False:
				if isinstance(address, (str)):
					address = self.address[address]
				return address
			else:
				print("ERREUR COMM: L'arduino", self.address[address], " n'est pas prête.")
				return -1
		else:
			print("ERREUR COMM: L'address: ", address, " est invalide.")
			return -1

	def checkOrder(self, order):
		"""verifie l'ordre et le convertie en int si nécessaire, sinon retourne -1"""
		if order in self.orders:
			if isinstance(order, (str)):
				order = self.orders[order]
			return order
		else:
			print("ERREUR COMM: L'ordre: ", order, " est invalide.")
			return -1

	def checkParsedOrderSize(self, order):
		"""check parsed sizes"""

		if order in self.argumentSize:#verification
			sizeExpected = self.argumentSize[order]
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
		else:
			print("ERREUR l'ordre ", order, "n'a pas été trouvé dans serial_defines.c")


	def checkOrderArgument(self, order, *arguments):
		"""check a given set of argument for an order, if all arguments type match return 0 else return -1"""

		if len(arguments) == len(self.ordersArguments[order]):
			for i, argumentType in enumerate(self.ordersArguments[order]):
				if argumentType == 'int':
					if not isinstance(arguments[i], (int)):
						print("L'argument ", i, " de l'ordre ", order, " n'est pas du bon type, attendu (int)")
						return -1
				elif argumentType == 'long':
					if not isinstance(arguments[i], (long)):
						print("L'argument ", i, " de l'ordre ", order, " n'est pas du bon type, attendu (long)")
						return -1
				elif argumentType == 'float':
					if not isinstance(arguments[i], (float)):
						print("L'argument ", i, " de l'ordre ", order, " n'est pas du bon type, attendu (float)")
						return -1
				else:
					print("ERREUR: l'argument parsé dans serial_define est de type inconnu")
					return -1
					
		else:
			print("ERREUR: l'order", order, "attend", len(self.ordersArguments[order]), "arguments, mais a recu:", len(arguments), "arguemnts")
			return -1

		return 0





	def sendOrderAPI(self, address, order, *arguments):
		""""api d'envoie d'ordres avec verification des parametres, retourne -1 en cas d'erreur, sinon 0"""
		
		if self.emptyFifo == True and order != self.orders['PINGPING_AUTO']:
			self.emptyFifo = False 
			self.timeStartProcessing = int(time.time()*1000)

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
		


	def readOrdersAPI(self, address='all'):
		"""Renvoi -1 si pas d'ordre en attente sinon renvoi un ordre """
		newOrderToRead = deque()
		find = False
		orderToReturn = -1
		self.mutexOrdersToRead.acquire()
		
		while len(self.ordersToRead) > 0:
			order = self.ordersToRead.pop()
			if (order[0] == address or order[0] == self.address[address] or address == 'all') and find == False:
				find = True
				orderToReturn = order
			else:
				newOrderToRead.append(order)

		self.mutexOrdersToRead.release()
		return orderToReturn
