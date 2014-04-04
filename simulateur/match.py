# -*- coding: utf-8 -*-


from geometry import ConvexPoly

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "objects"))

from define import *

points = {
	T_VERRE		:4,
	T_CERISE	:2,
	T_BOUGIE	:4,
	T_CADEAU	:4,
	T_FUNNY		:12
}

class Match:
	def __init__(self):
		self.carte_arrache = [0,0]

	def init(self, engine):
		self.engine = engine

	def score(self, team):
		score  =  points[T_VERRE]

		## TODO Complete score calculus
		return score



	
