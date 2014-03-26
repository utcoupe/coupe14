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



	def __repr__(self):
		return "Pos("+str(self.x)+","+str(self.y)+")"
