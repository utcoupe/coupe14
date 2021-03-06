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
		self.physicsengine.add_collision_handler(COLLTYPE_BRAS, COLLTYPE_TORCHE, self.__on_collision_bras_torche)
		self.physicsengine.add_collision_handler(COLLTYPE_BRAS_OUVRIR, COLLTYPE_FEU, self.__on_collision_bras_ouvrir_feu)
		self.physicsengine.add_collision_handler(COLLTYPE_BRAS_FERMER, COLLTYPE_FEU, self.__on_collision_bras_fermer_feu)
		self.physicsengine.add_collision_handler(COLLTYPE_BRAS_PETIT, COLLTYPE_FEU, self.__on_collision_bras_petit_feu)
		self.physicsengine.add_collision_handler(COLLTYPE_PETIT_ROBOT, COLLTYPE_WALL, self.graphicsengine.draw_collision)
		self.physicsengine.add_collision_handler(COLLTYPE_PETIT_ROBOT, COLLTYPE_FRESQUE, self.__on_collision_mini_fresque)
		self.e_stop = threading.Event()
		self.objects = []
		self.objects_to_remove = []
		self.__id_action_robot = 0

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

#==================================================
# Détail des méthodes appelées lors des collisions
#==================================================

	def __on_collision_gros_feu(self, space, arb):
		"""
		Quand le gros robot touche un feu
		"""
		robot = self.find_obj_by_shape(arb.shapes[0])
		if not robot:
			print("robot not found")
		else:
			feu = self.find_obj_by_shape(arb.shapes[1])
			if not feu:
				print("Feu not found")
			else:
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

	def __on_collision_bras_torche(self, space, arb):
		"""
		Quand le bras du gros robot touche un feu
		"""
		self.graphicsengine.draw_collision(space,arb)
		robot = self.find_obj_by_shape(arb.shapes[0])
		if not robot:
			print("bras not found")
		else:
			torche = self.find_obj_by_shape(arb.shapes[1])
			if not torche:
				print("Torche not found")
			else:
				id_tmp = robot.getLastIdOther()
				if id_tmp > self.__id_action_robot:
					feu = torche.prendreFeu()
					robot.setFeuHit(1) #positionne un flag pour dire qu'on a touché un triangle
					self.__id_action_robot = id_tmp

	def __on_collision_bras_ouvrir_feu(self, space, arb):
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
				xR,yR = robot.getPositionPixel()
				xF,yF = feu.getPositionPixel()
				if(feu.getOrientation() == 'vert'):
					if(xR < xF):
						feu.coucher('g','open')
					else:
						feu.coucher('d','open')
				else:
					if(yR < yF):
						feu.coucher('g','open')
					else:
						feu.coucher('d','open')

	def __on_collision_bras_fermer_feu(self, space, arb):
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
				xR,yR = robot.getPositionPixel()
				xF,yF = feu.getPositionPixel()
				if(feu.getOrientation() == 'vert'):
					if(xR < xF):
						feu.coucher('g','close')
					else:
						feu.coucher('d','close')
				else:
					if(yR < yF):
						feu.coucher('g','close')
					else:
						feu.coucher('d','close')

	def __on_collision_bras_petit_feu(self, space, arb):
		"""
		Quand le bras du petit robot touche un feu
		"""
		robot = self.find_obj_by_shape(arb.shapes[0])
		if not robot:
			print("bras not found")
		else:
			feu = self.find_obj_by_shape(arb.shapes[1])
			if not feu:
				print("Feu not found")
			else:
				xR,yR = robot.getPositionPixel()
				xF,yF = feu.getPositionPixel()
				if(feu.getOrientation() == 'vert'):
					if(xR < xF):
						feu.coucher('g','open')
					else:
						feu.coucher('d','open')
				else:
					if(yR < yF):
						feu.coucher('g','open')
					else:
						feu.coucher('d','open')

	def __on_collision_mini_fresque(self, space, arb):
		"""
		Quand le bras du petit robot touche un feu
		"""
		robot = self.find_obj_by_shape(arb.shapes[0])
		if not robot:
			print("bras not found")
		else:
			fresque = self.find_obj_by_shape(arb.shapes[1])
			if not fresque:
				print("Fresque not found")
			else:
				robot.accrocherFresques()

#=====================================================
# Détail des méthodes du moteur général.
# Regroupe les appels au moteur graphique et physique
#=====================================================

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
