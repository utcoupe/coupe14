#!/usr/bin/env python
# -*- coding: utf-8 -*-


import threading

#from ..define import *
from .motorphysic import MotorPhysic
from .motorgraphic import MotorGraphic

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))

from define import *


class Engine:
	"""
	Engine, cette classe permet de coupler un moteur physique et un
	moteur graphique.
	"""
	def __init__(self):
		"""
		@param stop_irc fonction permettant d'arreter le client irc (il
		tourne dans un thread à part).
		"""
		self.graphicsengine = MotorGraphic()
		self.physicsengine = MotorPhysic()
		self.physicsengine.add_collision_handler(COLLTYPE_GROS_ROBOT, COLLTYPE_WALL, self.graphicsengine.draw_collision)
		self.physicsengine.add_collision_handler(COLLTYPE_GROS_ROBOT, COLLTYPE_FEU, self.__on_collision_gros_feu)
		self.physicsengine.add_collision_handler(COLLTYPE_BRAS, COLLTYPE_FEU, self.__on_collision_bras_feu)
		self.physicsengine.add_collision_handler(COLLTYPE_PETIT_ROBOT, COLLTYPE_WALL, self.graphicsengine.draw_collision)
		self.e_stop = threading.Event()
		self.objects = []
		self.objects_to_remove = []
		self.e_stop = threading.Event()

	def init(self, match):
		self.match = match

	def find_obj_by_shape(self, shape):
		"""
		À partir d'une shape retrouve l'objet concerné
		"""
		for obj in self.objects:
			if obj.is_my_shape(shape):
				return obj
		return None

	def __on_collision_gros_feu(self, space, arb):
		"""
		Quand lle gros robot touche un feu
		"""
		robot = self.find_obj_by_shape(arb.shapes[0])
		if not robot:
			print("robot not found")
		else:
			feu = self.find_obj_by_shape(arb.shapes[1])
			if not feu:
				print("Feu not found")
			else:
				#print('feu eteindre')
				pass

	def __on_collision_bras_feu(self, space, arb):
		"""
		Quand le bras du gros robot touche un feu
		"""
		robot = self.find_obj_by_shape(arb.shapes[0])
		if not robot:
			print("bras not found")
		else:
			feu = self.find_obj_by_shape(arb.shapes[1])
			if not feu:
				print("Feu not found")
			else:
				robot.setFeuHit(1) #positionne un flag pour dire qu'on a touché un triangle
				feu.eteindre() #supprime le feu de la map

	def stop(self):
		self.e_stop.set()
	
	def start(self):
		"""
		Démarrer l'engine
		"""
		while not self.e_stop.is_set():
			try:
				self.step()
			except KeyboardInterrupt as ex:
				print("Exit")
				break

	def step(self):
		"""
		Effectuer un step
		"""
		for o in self.objects_to_remove:
			if o: self.remove(o)
		self.objects_to_remove = []
		dt = 1.0/float(FPS)
		self.physicsengine.step(dt)
		if not self.graphicsengine.step():
			self.stop()
			
	def add(self, obj):
		"""
		Ajouter un objet à l'engine, il est ajouté du même coup au moteur
		physique et au moteur graphique.
		"""
		self.objects.append(obj)
		self.graphicsengine.add(obj)
		self.physicsengine.add(obj)

	def add_extension(self, obj):
		if not obj.is_extension:
			raise Exception("add_extension can be used only on an extension")
		else:
			self.graphicsengine._add_extension(obj)
			self.physicsengine._add_extension(obj)

	def remove(self, obj):
		if obj.is_extension:
			self.remove_extension(self)
		else:
			for o in obj.extension_objects:
				self.remove_extension(o)
			self.graphicsengine.remove(obj)
			self.physicsengine.remove(obj)
			self.objects.remove(obj)

	def remove_extension(self, obj):
		if not obj.is_extension:
			raise Exception("remove_extension can only be used on an extension object")
		else:
			self.graphicsengine.remove_extension(obj)
			self.physicsengine.remove_extension(obj)
