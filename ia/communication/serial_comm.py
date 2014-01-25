# -*- coding: utf-8 -*-

"""
	Gére la communication par le port serie

"""

import serial
from collections import deque
import conversion

class ComSerial():
	def __init__(self, name, baudrate):
		self.liaison = serial.Serial(name, baudrate, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE)
		self.rawInput = ""
		self.readyToRead = False

	def read(self):
		"""La fonction retourne une liste de chaine de char, qui ont pour en-tête 1XXXXXXX et pour fin fin 10000000"""
		rawInputList = deque()

		if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé')
		else:
			if self.liaison.inWaiting():
				self.rawInput += self.liaison.read(self.liaison.inWaiting())
			

			#on crée un variable temporaire
			chaineDeBoucle = []
			i = 0
			for leter in self.rawInput:
				chaineDeBoucle.append(self.rawInput[i])
				i += 1

			i = 0
			self.readyToRead = False
			for leter in chaineDeBoucle:
				value = ord(leter)

				if value > 128:#c'est forcement le premier paquet
					if value > 192: # si c'est un packet de reset
						rawInputList.append(leter)
						self.rawInput = self.rawInput[i+1:]
						self.readyToRead = False
						i = 0
						
					else: #si c'est un paquet de debut de trame
						self.rawInput = self.rawInput[i:]#également si on a perdu le paquet de fin
						self.readyToRead = True
						i = 0	
									
				if value == 128:
					if self.readyToRead == True:#cas normal
						rawInputList.append(self.rawInput[:i+1])
					self.rawInput = self.rawInput[i:]#également quand on a perdu le paquet de debut
					self.readyToRead = False
					i = 0

				i += 1
		return rawInputList

	def send(self, rawOutputString):
		""" rawInputList doit être une liste de chaine de char, qui ont pour en-tête 1XXXXXXX et pour fin fin 10000000""" 
		if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé k')
		else:
			#Affichage de debug
			for char in rawOutputString:
				temp = bin(ord(char))[2:]
				while len(temp) < 8:
					temp = '0' + temp

			self.liaison.write(rawOutputString)

