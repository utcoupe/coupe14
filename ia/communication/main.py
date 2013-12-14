# -*- coding: utf-8 -*-
"""
Ce fichier gère la communication
"""


import parser_c

class communication():
	def __init__(self):
		self.address = {}
		self.orders = {}
		self.ordersSize = {}
		parser_c.parseConstante(self.address, self.orders, self.ordersSize)

	def printDico(self):
		print(self.address)
		print(self.orders)
		print(self.ordersSize)


instance = communication()
instance.printDico()