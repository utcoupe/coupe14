# -*- coding: utf-8 -*-
"""
Ce fichier contient les structures de données 
"""

class Position():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def distanceSquarred(self, pos):
		return (self.x-pos.x)**2 + (self.y-pos.y)**2

	def add(self, pos):
		return Position(pos.x+self.x, pos.y+self.y)
	def subtract(self, pos):
		return Position(pos.x-self.x, pos.y-self.y)
	def multiply(self, coeff):
		self.x *= coeff
		self.y *= coeff
		return self


	def __repr__(self):
		return "Pos("+str(self.x)+","+str(self.y)+")"
