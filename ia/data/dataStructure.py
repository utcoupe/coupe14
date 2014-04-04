# -*- coding: utf-8 -*-
"""
Ce fichier contient les structures de données 
"""

class Position():
	def __init__(self, arg1, y=None):
		if isinstance(arg1, Position):
			self.x = arg1.x
			self.y = arg1.y
		else:
			if y == None:
				print("Position:missing y parameter with first param("+arg1+") != Position")
			self.x = arg1
			self.y = y


	def distanceSquarred(self, pos):
		return (self.x-pos.x)**2 + (self.y-pos.y)**2

	def add(self, pos): #return self
		self.x += pos.x
		self.y += pos.y
		return self
	def subtract(self, pos): #return self
		self.x -= pos.x
		self.y -= pos.y
		return self
	def multiply(self, coeff): #return self
		self.x *= coeff
		self.y *= coeff
		return self


	def __repr__(self):
		return "Pos("+str(self.x)+","+str(self.y)+")"
