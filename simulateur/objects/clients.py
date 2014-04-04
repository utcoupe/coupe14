# -*- coding: utf-8 -*-

import sys
import os
import math
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *

class GoalPWM:
	def __init__(self, pwm, delay):
		self.pwm = pwm
		self.delay = delay
		self.start = -1

class GoalPOS:
	def __init__(self, x, y):
		"""
		@param {int:px} x
		@param {int:px} y
		"""
		self.pos = (x,y)


class GoalANGLE:
	def __init__(self, a):
		"""
		@param {float:radians} a
		"""
		self.a = a


class GoalPOSR(GoalPOS): pass
class GoalANGLER(GoalANGLE): pass

#########################################################################
# clients qui emulent les clients physiques (asserv, visio, others)
#########################################################################

class Asserv:
	""" Émule l'arduino dédiée à l'asservissement """
	def __init__(self, robot):
		self.__robot = robot

	def adresse(self):
		#TODO return en fonction de l'enum
		if self.__robot.getTyperobot == BIG:
			return 2
		elif self.__robot.getTyperobot == MINI:
			return 5

	def ping(self):
		return 'asserv pong'

	def goto(self, x, y):
		"""
		Donner l'ordre d'aller à un point
		@param x mm
		@param y mm
		"""
		self.__robot.addGoal(GoalPOS(*mm_to_px(x,y)))

	def gotor(self, x, y):
		"""
		Donner l'ordre d'aller à un point, relativement à la position actuelle
		@param x mm
		@param y mm
		"""
		self.__robot.addGoal( GoalPOSR(*mm_to_px(x,y)))

	def gotoa(self, x, y, a):
		"""
		Donner l'ordre d'aller à un point et de tourner d'un angle
		@param x mm
		@param y mm
		@param a rad
		"""
		self.__robot.addGoal(GoalPOS(*mm_to_px(x,y)))
		self.__robot.addGoal(GoalANGLE(math.radians(a)))

	def gotoar(self, x, y, a):
		"""
		Donner l'ordre d'aller à un point et de tourner d'un angle,relativement à la position actuelle
		@param x mm
		@param y mm
		@param a rad
		"""
		self.__robot.addGoal(GoalPOSR(*mm_to_px(x,y)))
		self.__robot.addGoal(GoalANGLER(math.radians(a)))

	def rot(self, a):
		"""
		Donner l'ordre de tourner d'un angle
		@param a rad
		"""
		self.__robot.addGoal(GoalANGLE(math.radians(a)))

	def rotr(self, a):
		"""
		Donner l'ordre de tourner d'un angle,relativement à l'angle actuel
		@param a rad
		"""
		self.__robot.addGoal(GoalANGLER(math.radians(a)))

	def cleang(self):
		"""
		Donner l'ordre de clean la pile de goals
		"""
		self.__robot.cleanGoals()
		return 0

	def stop(self):
		"""
		Donner l'ordre de stopper le robot
		"""
		self.__robot.setStop(True)
		return 0

	def resume(self):
		"""
		Donner l'ordre de reprendre le robot
		"""
		self.__robot.setStop(False)
		return 0

	def getPos(self):
		"""
		Demande de retourner la position actuelle du robot (x, y, angle)
		@return int position x du robot
		@return int position y du robot
		@return float angle du robot
		"""
		return self.__robot.x(), self.__robot.y(), self.__robot.a()

	def pwm(self, pwm_l, pwm_r, delay):
		"""
		Demande à avance en pwm
		@param pwm_l int (0 - 255)
		@param delay s
		"""
		self.__robot.addGoal(GoalPWM(pwm_l, delay/1000))

class Visio:
	"""Émule le programme de visio"""

	def __init__(self, robot):
		self.__robot = robot

	def ping(self):
		return "visio pong"

	def adresse(self):
		#TODO return en fonction de l'enum
		return 3

class Others:
	""" Émule l'arduino dédiée aux others """
	def __init__(self, robot):
		self.__robot = robot

	def ping(self):
		return "others pong"

	def adresse(self):
		#TODO return en fonction de l'enum
		if self.__robot.getTyperobot == BIG:
			return 1
		elif self.__robot.getTyperobot == MINI:
			return 4