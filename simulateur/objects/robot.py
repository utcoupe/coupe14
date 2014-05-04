# -*- coding: utf-8 -*-


import random
import math
import time
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

from define import *
from engine.engineobject import EngineObjectPoly
from .clients import *

class Robot(EngineObjectPoly):
	def __init__(self, *, engine, team, posinit, mass, poly_points,
				 typerobot, extension_objects=[], colltype):
		color = 'yellow' if team == YELLOW else 'red'
		EngineObjectPoly.__init__(self,
			engine		 	= engine,
			mass			= mass,
			posinit			= posinit,
			color			= color,
			colltype		= colltype, 
			poly_points		= poly_points,
			extension_objects	= extension_objects
		)

	#données d'état du robot
		self.__typerobot = typerobot
		self.__team = team
		self.__goals = []
		self.__asserv = Asserv(self)
		self._visio = Visio(self)
		self.__others = Others(self)


	#données du robot utiles au simulateur
		self.__mod_teleport = False # quand on clique ça téléporte au lieu d'envoyer un ordre à l'asservissement
		self.__mod_recul = False # marche arrière ou marche avant ?
		self.__max_speed = 1000 # vitesse maximale (quand pwm=255)
		self.__stop = False

		#utilité ?
		self.__current_team = RED
		self.__current_robot = BIG

		self.body._set_velocity_func(self._my_velocity_func())

	def init(self, engine):
		self.__engine = engine

	def getXreal(self):
		"""
		Renvoie la position x réelle du robot (pas celle simulée)
		"""
		return px_to_mm(self.body.position[0])
	
	def getYreal(self):
		"""
		Renvoie la position y réelle du robot (pas celle simulée)
		"""
		return 2000 - px_to_mm(self.body.position[1])
	
	def getAreal(self):
		"""
		Renvoie l'angle a réel du robot (pas celle simulée)
		"""
		return - self.body.angle

	def setXsimu(self, x):
		"""
		Positionne la valeur de x simulée (à partir de la réelle)
		@param x valeur en mm (réelle)
		"""
		self.body.position[0] = mm_to_px(x)

	def setYsimu(self, y):
		"""
		Positionne la valeur de y simulée (à partir de la réelle)
		@param y valeur en mm (réelle)
		"""
		self.body.position[1] = mm_to_px(2000 - y)

	def setAsimu(self, a):
		"""
		Positionne la valeur de a simulée (à partir de la réelle)
		@param a valeur en mm (réelle)
		"""
		self.body.angle = -a

	def getPositionPixel(self):
		return self.body.position[0], self.body.position[1]

	def getPosition(self):
		return self.getXreal(), self.getYreal(), self.getAreal()

	def getPositionId(self):
		return self.getXreal(), self.getYreal(), self.getAreal(), self.__asserv.getLastIdAction()

	def getLastIdAsserv(self):
		return self.__asserv.getLastIdAction()

	def getLastIdOther(self):
		return self.__others.getLastIdAction()

	def setLastIdActionAsserv(self, id):
		self.__asserv.setLastIdAction(id)

	def setlastIdActionOther(self, id):
		self.__others.setLastIdAction(id)

	def resetIdAsserv(self):
		self.__asserv.resetLastIdAction()

	def resetIdOther(self):
		self.__others.resetLastIdAction()

	def getTyperobot(self):
		return self.__typerobot

	def getTeam(self):
		return self.__team

	def addGoal(self, newGoal):
		self.__goals.append(newGoal)

	def cleanGoals(self):
		self.__goals = []

	def setStop(self, value):
		self.__stop = value

	def setPosition(self, x, y, a):
		#print('set pos x : ', x, ' y : ', y, ' a : ', a)
		self.setXsimu(x)
		self.setYsimu(y)
		self.setAsimu(a)

	def addGoalOrder(self, numOrdre, arg):
		"""
		Méthode appelée depuis communication pour ajouter un goal au robot
		Lors des appel aux commandes de l'asserv, il faut passer en paramètre
		les coordonnées en simulé, pas en réel.
		@param numOrdre int définit dans define
		@param args x, y ou a en réel
		"""
		if (numOrdre == GOTO):
			self.__asserv.goto(arg[0], arg[1],2000-arg[2])
		elif (numOrdre == GOTOA):
			self.__asserv.gotoa(arg[0], arg[1],2000-arg[2],-arg[3])
		elif (numOrdre == GOTOAR):
			self.__asserv.gotoar(arg[0], arg[1],2000-arg[2],-arg[3])
		elif (numOrdre == GOTOR):
			self.__asserv.gotor(arg[0], arg[1],2000-arg[2])
		elif (numOrdre == ROT):
			self.__asserv.rot(arg[0], -arg[1])
		elif (numOrdre == ROTR):
			self.__asserv.rotr(arg[0], -arg[1])
		elif (numOrdre == PWM):
			self.__asserv.pwm(arg[0], arg[1], arg[2], arg[3])	#!! x=pwm_l, y=pwm_r, angle=delay !!

	def _my_velocity_func(self):
		"""
		Fonction qui détermine la vitesse des corps.
		Tous les traitements se font avec les coordonnées du simulateur (pas les réelles)
		"""
		def f(body, gravity, damping, dt):
			self.body._set_torque(0)
			self.body._set_angular_velocity(0)
			if not self.__stop and self.__goals:
				current_goal = self.__goals[0]
				if isinstance(current_goal, GoalPOSR):
					x,y = self.body.position
					a = self.body.angle
					cx, cy = current_goal.pos
					dx = cx * math.cos(a) - cy * math.sin(a)
					dy = cx * math.sin(a) + cy * math.cos(a)
					self.__goals[0] = GoalPOS(x+dx, y+dy)
				elif isinstance(current_goal, GoalANGLER):
					a = current_goal.a
					ca = self.body.angle
					self.__goals[0] = GoalANGLE(ca+a)
				elif isinstance(current_goal, GoalPOS):
					gx,gy = current_goal.pos
					v = self.__max_speed / 4
					x,y = self.body.position
					dx = gx - x
					dy = gy - y
					d = math.sqrt(dx**2+dy**2)
					if d < abs(v * dt):
						self.body._set_position((gx,gy))
						removed_goal = self.__goals.pop(0)
						self.__asserv.setLastIdAction(removed_goal.id_action)
						self.body._set_velocity((0,0))
					else:
						a = math.atan2(dy, dx)
						vx = abs(v) * math.cos(a)
						vy = abs(v) * math.sin(a)
						self.body._set_velocity((vx,vy))
						if v < 0:
							a += math.pi
						abot = self.body.angle
						if a > abot:
							diff = a - abot
						else:
							diff = abot - a
						#print('différence : ', diff)
						if (abs(diff) < 0.5):
							#print('angle petit : ', a)
							self.body._set_angle(a)
						else:
							#print('angle grand : ', a)
							self.__goals.insert(0, GoalANGLE(0,a))
				elif isinstance(current_goal, GoalPWM):
					if current_goal.start == -1:
						current_goal.start = time.time()
					elif (time.time() - current_goal.start) > current_goal.delay:
						removed_goal = self.__goals.pop(0)
						self.__asserv.setLastIdAction(removed_goal.id_action)
					else:
						a = self.body.angle
						v = self.__max_speed * current_goal.pwm / (255*8)
						vx = v * math.cos(a)
						vy = v * math.sin(a)
						self.body._set_velocity((vx,vy))
				elif isinstance(current_goal, GoalANGLE):
					self.body._set_velocity((0,0))
					goala = current_goal.a
					cura = self.body.angle
					difference_value_1 = (cura - goala)
					difference_value_2 = (cura + goala)
					if abs(difference_value_1) > abs(difference_value_2):
						diffrence_value = difference_value_2
					else:
						diffrence_value = difference_value_1
					#print('goal ANGLE, current : ', cura, ' goal : ', goala, ' diff : ',diffrence_value)
					if (abs(diffrence_value) < 0.1):
						self.body._set_angle(current_goal.a)
						removed_goal = self.__goals.pop(0)
						self.__asserv.setLastIdAction(removed_goal.id_action)
						self.body._set_angular_velocity(0)
					else:
						vitesse_angulaire = 4 #valeur choisie pour avoir vitesse angulaire simu proche du réel
						if (diffrence_value > 0):
							self.body._set_angular_velocity(-vitesse_angulaire)
						else:
							self.body._set_angular_velocity(vitesse_angulaire)
				else:
					raise Exception("type_goal inconnu")
			else:
				self.body._set_velocity((0,0))
		return f

	def onEvent(self, event):
		# selection des teams et des robots
		if KEYDOWN == event.type:
			if KEY_CHANGE_TEAM == event.key:
				self.__current_team = RED
				print("équipe rouge")
				return True
			elif KEY_CHANGE_ROBOT == event.key:
				self.__current_robot = MINI
				print("control du mini robot")
				return True
			elif KEY_TELEPORTATION == event.key:
				self.__mod_teleport = not self.__mod_teleport
				return True
			elif KEY_RECUL == event.key:
				self.__mod_recul = not self.__mod_recul
			elif KEY_JACK == event.key:
				#todo avertir jack unplugged
				pass
		elif KEYUP == event.type:
			if KEY_CHANGE_TEAM == event.key:
				print("équipe jaune")
				self.__current_team = YELLOW
				return True
			elif KEY_CHANGE_ROBOT == event.key:
				self.__current_robot = BIG
				print("control gros robot")
				return True

		# actions
		if self._event_concerns_me(event):
			# keydown
			if KEYDOWN == event.type:
				if KEY_STOP_RESUME == event.key:
					self.__asserv.stop()
					return True
				elif KEY_CANCEL == event.key:
					self.__asserv.cleang()
					return True
			# keyup
			elif KEYUP == event.type:
				if KEY_STOP_RESUME == event.key:
					self.__asserv.resume()
			# mouse
			elif MOUSEBUTTONDOWN == event.type:
				p = event.pos
				p_mm = px_to_mm(p)
				if self.__mod_teleport:
					#self.extras.teleport(p_mm[0], p_mm[1], 0)
					print ('pass dans le mod teleport')
				else:
					v = mm_to_px(1000) * (-1 if self.__mod_recul else 1)
					#on clean les goals avant d'en envoyer un nouveau afin d'éviter les blocages
					self.cleanGoals()
					self.__asserv.goto(0,*px_to_mm(p[0],p[1]))
				return True
		return False

	def _event_concerns_me(self, event):
		return self.__current_team == self.__team and self.__typerobot == self.__current_robot
	
	def __repr__(self):
		return "Robot"