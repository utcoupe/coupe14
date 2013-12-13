# -*- coding: utf-8 -*-

"""
	Gére la communication par le port serie

"""

import serial


class comSerial:
	def __init__(self, name, baudrate):
		self.liaison = serial.Serial()
		try:
			self.liaison = serial.Serial(name, baudrate)
		except:
			print('Impossible de d\'initializer:', name, 'à', baudrate)

	def read(self):
		if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé')

		info = self.liaison.read(1) #On le lit le premier octet
		print(info)

	def send(self, commande, *parametres):
		if self.liaison.isOpen() == False:
			print('comSerial,fct send: La liaison demandé n\'a pas été initializé k')

		print(commande)
		for param in parametres:
			print(param)

ser = comSerial('/dev/ttyACMS', 115200)
ser.send('avance à la position', (100,100),(250,250))
