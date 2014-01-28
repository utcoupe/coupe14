# -*- coding: utf-8 -*-

"""
	Gére la communication par le port serie

"""

import serial
from collections import deque
from . import conversion
import binascii

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
				#self.rawInput += self.liaison.read(self.liaison.inWaiting())
				temp = self.liaison.read(self.liaison.inWaiting())
				for letter in temp:
						self.rawInput += chr(letter)

				i = 0
				debutChaine = 0
				self.readyToRead = False
				for leter in self.rawInput:
					value = ord(leter)

					if value > 128:#c'est forcement le premier paquet
						if value > 192: # si c'est un packet de reset
							rawInputList.append(leter)
							self.readyToRead = False
							debutChaine = i+1
							
							
						else: #si c'est un paquet de debut de trame
							#également si on a perdu le paquet de fin
							self.readyToRead = True
							debutChaine = i
								
										
					if value == 128:
						if self.readyToRead == True:#cas normal
							rawInputList.append(self.rawInput[debutChaine:i+1])
						#également quand on a perdu le paquet de debut
						self.readyToRead = False
						debutChaine = i
						

					i += 1
				self.rawInput = self.rawInput[debutChaine:]
		return rawInputList

	def send(self, rawOutputString):
		""" rawInputList doit être une liste de chaine de char, qui ont pour en-tête 1XXXXXXX et pour fin fin 10000000""" 
		if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé k')
		else:
			#Affichage de debug
			formatedString = ""
			for char in rawOutputString:
				self.liaison.write(bytes(char, 'latin-1'))
				#bytes(char, 'latin-1'))
				"""temp = bin(ord(char))[2:]
				while len(temp) < 8:
					temp = '0' + temp
				formatedString += conversion.binaryToInt(temp)
			
			#encodedArray = rawOutputString.encode("Utf-8") 
			#encodedArray = binascii.a2b_uu(rawOutputString)
			#ser.write(bytes(Vcorrt.encode('ascii')))
			for letter in rawOutputString:
				#print(bytes(chr(letter), 'latin-1'))
				self.liaison.write(bytes(chr(letter), 'latin-1'))"""

