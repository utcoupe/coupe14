# -*- coding: utf-8 -*-

"""
	Gére la communication par le port serie

"""

import serial
from collections import deque
from . import conversion
import binascii

class ComSerial():
	def __init__(self, name, baudrate, parity):
		if parity == 'ODD':
			self.liaison = serial.Serial(name, baudrate, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE)
		else if parity == 'NONE':
			self.liaison = serial.Serial(name, baudrate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
		else:
			print('Parity ', parity, ' non valide');
		self.rawInput = []
		self.readyToRead = False

	def read(self):
		"""La fonction retourne une liste de chaine de char, qui ont pour en-tête 1XXXXXXX et pour fin fin 10000000"""

		"""if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé')"""

		rawInputList = deque()
		if self.liaison.inWaiting():
			#self.rawInput += self.liaison.read(self.liaison.inWaiting())
			self.rawInput += self.liaison.read(self.liaison.inWaiting())

			i = 0
			debutChaine = 0
			self.readyToRead = False
			for leter in self.rawInput:

				if leter > 128:#c'est forcement le premier paquet,
					if leter > 192: # si c'est un packet de reset,
						rawInputList.append([leter])
						self.readyToRead = False
						debutChaine = i+1
						
						
					else: #si c'est un paquet de debut de trame
						#également si on a perdu le paquet de fin
						self.readyToRead = True
						debutChaine = i
							
									
				if leter == 128:
					if self.readyToRead == True:#cas normal
						#TODO return int instead of chr to avoid converting
						
						rawInputList.append(self.rawInput[debutChaine:i+1])
					#également quand on a perdu le paquet de debut
					self.readyToRead = False
					debutChaine = i
					

				i += 1
			self.rawInput = self.rawInput[debutChaine:]
		return rawInputList

	def send(self, rawOutputString):
		""" rawInputList doit être une liste de chaine de char, qui ont pour en-tête 1XXXXXXX et pour fin 10000000""" 
		"""if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé k')"""
		
		for char in rawOutputString:
			self.liaison.write(bytes(char, 'latin-1'))
			print(conversion.intToBinary(ord(char))[:8])
			

