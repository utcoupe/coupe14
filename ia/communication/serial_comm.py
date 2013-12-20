# -*- coding: utf-8 -*-

"""
	Gére la communication par le port serie

"""

import serial
from collections import deque

class ComSerial():
	def __init__(self, name, baudrate):
		self.liaison = serial.Serial(name, baudrate, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE)
		self.rawInput = ""
		self.readyToRead = False

	def read(self):
		"""La fonction retourne une liste de chaine de char, qui ont pour en-tête 1XXXXXXX et pour fin fin 10000000"""
		rawInputList =deque()
		packetAddress = 0

		if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé')
		else:
			if self.liaison.inWaiting():
				self.rawInput += self.liaison.read(self.liaison.inWaiting())
			i = 0
			for leter in self.rawInput:
				value = ord(leter)

				#detection les paquets qui commencent pas 1 car il delimites les trames
				if value > 128: #si c'est un paquet de debut de trame
					if self.readyToRead == False:
						self.readyToRead = True
					else: #si on a perdu le paquet de fin
						self.rawInput = self.rawInput[i:]
						i = 0			
				if value == 128:
					if self.readyToRead == True:#cas normal
						self.readyToRead = False
						rawInputList.append(self.rawInput[:i+1])
						self.rawInput = self.rawInput[i+1:]
						i = 0
					else: # on a perdu le paquet de debut
						self.rawInput = self.rawInput[i:]
						i = 0
				i += 1
		return rawInputList

	def send(self, rawOutputList):
		""" rawInputList doit être une liste de chaine de char, qui ont pour en-tête 1XXXXXXX et pour fin fin 10000000""" 
		if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé k')
		else:
			for rawOutput in rawOutputList:
				self.liaison.write(rawOutput)

