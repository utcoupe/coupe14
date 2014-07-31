# -*- coding: utf-8 -*-

import sys
import os
import math
import time
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))
from define import *


#=========================================================================

#Regroupe diverses classes utiles pour le fonctionnement du simulateur.
#Regroupe aussi les clients du robot (asserv, visio, others).

#=========================================================================


class GoalPWM:
	def __init__(self, id_action, pwm, delay):
		self.id_action = id_action
		self.pwm = pwm
		self.delay = delay
		self.start = -1

class GoalPOS:
	def __init__(self, id_action, x, y):
		"""
		@param {int:px} x
		@param {int:px} y
		"""
		self.id_action = id_action
		self.pos = (x,y)


class GoalANGLE:
	def __init__(self, id_action, a):
		"""
		@param {float:radians} a
		"""
		self.id_action = id_action
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
		self.__last_id_action_executed = -1

	def resetLastIdAction(self):
		self.__last_id_action_executed = -1

	def setLastIdAction(self, id):
		self.__last_id_action_executed = id

	def getLastIdAction(self):
		return self.__last_id_action_executed

	def adresse(self):
		if self.__robot.getTyperobot == BIG:
			return 2
		elif self.__robot.getTyperobot == MINI:
			return 5

	def ping(self):
		return 'asserv pong'

	def goto(self, id_action, x, y):
		"""
		Donner l'ordre d'aller à un point
		@param x mm
		@param y mm
		"""
		self.__robot.addGoal(GoalPOS(id_action, *mm_to_px(x,y)))

	def gotor(self, id_action, x, y):
		"""
		Donner l'ordre d'aller à un point, relativement à la position actuelle
		@param x mm
		@param y mm
		"""
		self.__robot.addGoal( GoalPOSR(id_action, *mm_to_px(x,y)))

	def gotoa(self, id_action, x, y, a):
		"""
		Donner l'ordre d'aller à un point et de tourner d'un angle
		@param x mm
		@param y mm
		@param a rad
		"""
		self.__robot.addGoal(GoalPOS(id_action, *mm_to_px(x,y)))
		self.__robot.addGoal(GoalANGLE(id_action, a))

	def gotoar(self, id_action, x, y, a):
		"""
		Donner l'ordre d'aller à un point et de tourner d'un angle,relativement à la position actuelle
		@param x mm
		@param y mm
		@param a rad
		"""
		self.__robot.addGoal(GoalPOSR(id_action, *mm_to_px(x,y)))
		self.__robot.addGoal(GoalANGLER(id_action, a))

	def rot(self, id_action, a):
		"""
		Donner l'ordre de tourner d'un angle
		@param a rad
		"""
		#print('rot : a = ', a)
		self.__robot.addGoal(GoalANGLE(id_action, a))

	def rotr(self, id_action, a):
		"""
		Donner l'ordre de tourner d'un angle,relativement à l'angle actuel
		@param a rad
		"""
		self.__robot.addGoal(GoalANGLER(id_action, a))

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
		return self.__robot.getXreal(), self.__robot.getYreal(), self.__robot.getAreal()

	def pwm(self, id_action, pwm_l, pwm_r, delay):
		"""
		Demande à avance en pwm
		@param pwm_l int (0 - 255)
		@param delay s
		"""
		self.__robot.addGoal(GoalPWM(id_action, pwm_l, delay/1000))

class Visio:
	"""
	Émule le programme de visio.
	Ne sera pas utilisé dans le simulateur 2014 pour des raisons d'architecture.
	(la visio est intégrée à l'IA sans passer par le protocole)
	"""

	def __init__(self, robot):
		self.__robot = robot

	def ping(self):
		return "visio pong"

	def adresse(self):
		return 3

	def actionBras(self):
		"""
		zone dans laquelle le bras du robot peut choper un triangle
		quand il y a un triangle dans la zone, celui-ci est supprimé
		"""
		self.__robot.add_bras()
		time.sleep(0.5) #temps où le bras apparaitra
		self.__robot.remove_bras()

class Others:
	""" Émule l'arduino dédiée aux others """
	def __init__(self, robot):
		self.__robot = robot
		self.__last_id_action_executed = -1

	def resetLastIdAction(self):
		self.__last_id_action_executed = -1

	def setLastIdAction(self, id):
		self.__last_id_action_executed = id

	def getLastIdAction(self):
		return self.__last_id_action_executed

	def ejectTriangle(self):
		self.__robot.releaseFeu()

	def ping(self):
		return "others pong"

	def adresse(self):
		if self.__robot.getTyperobot == BIG:
			return 1
		elif self.__robot.getTyperobot == MINI:
			return 4