# -*- coding: utf-8 -*-


import math

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "map"))

import pygame as pg
from pygame.locals import *
from pygame.color import *
from define import  *

from .engineobject import CIRCLE, POLY, WALL



class MotorGraphic():	
	def __init__(self):
		print("IN : Cstr MotorGraphic")
		pg.init()
		self.screen = pg.display.set_mode(mm_to_px(3000, 2000))
		self.clock = pg.time.Clock()
		self.objects = []
		self.onEvents = []
		self.collisions_to_draw = []
		self.map_img = pg.image.load("map/map.bmp")
		self.map_img=pg.transform.scale(self.map_img,(self.screen.get_width(),self.screen.get_height()))
		print("OUT : Cstr MotorGraphic")

	def draw_obj(self, obj):
		#print("IN : MotorGraphic::draw_obj")
		if obj.t == CIRCLE:
			self.draw_circle_from_obj(obj.shape, THECOLORS[obj.color])
		elif obj.t == POLY:
			self.draw_poly_from_obj(obj.shape, THECOLORS[obj.color])
		elif obj.t == WALL:
			self.draw_segment_from_obj(obj.shape, THECOLORS[obj.color])
		else:
			raise Exception("MotorGraphic.draw_obj : type '%s' doesn't exist"%obj.t)
		for o in obj.extension_objects:
			self.draw_obj(o)

	def step(self):
		#print("IN : MotorGraphic::step")
		### Clear screen
		self.screen.fill(THECOLORS["white"])
		
		### Draw background
		self.screen.blit(self.map_img,(0,0))

		### Draw debug
		"""self.debug.lock.acquire()
		for d in self.debug.circles.values():
			for o in d.values():
				self.draw_circle(o.position, o.radius, o.color)
		for d in self.debug.segments.values():
			for o in d.values():
				self.draw_segment(o.p1, o.p2, o.color)
		self.debug.lock.release()"""

		### Draw
		for obj in self.objects:
			self.draw_obj(obj)
		### Draw collisions
		for p,r in self.collisions_to_draw:
			pg.draw.circle(self.screen, THECOLORS["red"], p, r, 0)
		self.collisions_to_draw = []
		### Flip screen
		#print("avant flip screen")
		pg.display.flip()
		self.clock.tick(FPS)
		pg.display.set_caption( "fps: " + str(self.clock.get_fps()))
		#print(str(self.clock.get_fps()))
		#print("après flipscreen")
		### Events
		for event in pg.event.get():
			if event.type == QUIT:
				return False
			else:
				for f in self.onEvents: f(event)
		#print("OUT : step")
		return True

	def draw_circle_from_obj(self, shape, color):
		#print("IN : MotorGraphic::draw_circle_from_obj")
		p = tuple(map(int, shape.body.position))
		self.draw_circle(p, int(shape.radius), color)

	def draw_circle(self, p, r, color):
		#print("IN : MotorGraphic::draw_circle")
		pg.draw.circle(self.screen, color, p, r, 0)
	
	def draw_poly_from_obj(self, shape, color):
		#print("IN : MotorGraphic::draw_poly_from_obj")
		body = shape.body
		ps = shape.get_vertices()
		self.draw_poly(ps, color)

	def draw_poly(self, points, color):
		#print("IN : MotorGraphic::draw_poly")
		pg.draw.polygon(self.screen, color, points, 0)

	def draw_segment_from_obj(self, shape, color):
		#print("IN : MotorGraphic::draw_segment_from_obj")
		body = shape.body
		p1 = body.position + shape.a.rotated(body.angle)
		p2 = body.position + shape.b.rotated(body.angle)
		self.draw_segment(p1, p2, color)

	def draw_segment(self, p1, p2, color):
		#print("IN : MotorGraphic::draw_segment")
		pg.draw.lines(self.screen, color, False, [p1,p2])
	
	def draw_collision(self, space, arb):
		#print("IN : MotorGraphic::draw_collision")
		for c in arb.contacts:
			r = 5 #min(10, max( 3, abs(c.distance*5) ))
			r = int(r)
			p = tuple(map(int, c.position))
			self.collisions_to_draw.append((p, r))

	def add(self, obj):
		#print("IN : MotorGraphic::add")
		if obj.is_extension:
			raise Exception("you can only add a main object to the graphics engine")
		self.objects.append(obj)
		try:
			self.onEvents.append(obj.onEvent)
		except:
			pass
		for o in obj.extension_objects:
			self._add_extension(o)
			
	def _add_extension(self, obj):
		#print("IN : MotorGraphic::_add_extension")
		if not obj.is_extension:
			raise Exception("add_extension can be used only on an extension")
		try:
			self.onEvents.append(obj.onEvent)
		except:
			pass
		for o in obj.extension_objects:
			self._add_extension(o)

	def remove(self, obj):
		#print("IN : MotorGraphic::remove")
		if obj.is_extension:
			self.remove_extension(obj)
		else:
			self.objects.remove(obj)

	def remove_extension(self, obj):
		#print("IN : MotorGraphic::remove_extension")
		if not obj.is_extension:
			raise Exception("remove_extension can only be used on an extension object")
		else:
			pass
	
