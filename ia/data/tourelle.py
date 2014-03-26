# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""

from .dataStructure import *
from constantes import *

class Tourelle():
	def __init__(self, Flussmittel, Tibot, BigEnemyBot, SmallEnemyBot, communication, arduinoConstantes, address):
		self.Flussmittel = Flussmittel
		self.Tibot = Tibot
		self.BigEnemyBot = BigEnemyBot
		self.SmallEnemyBot = SmallEnemyBot
		self.__communication = communication
		self.__address = address

		#Variables
		self.__old_data_position = []
		self.__old_data_timestamp = []
		
	"""
	def getLastDataPosition(self):
		return self.__last_data_position
	"""

	def majPosition(self, arguments):
		#print("debug:arguments"+str(arguments)+"\n")
		timestamp = arguments[0]

		position_nos_robots = []
		if self.Flussmittel is not None:
			temp = self.Flussmittel.getPositon
			position_nos_robots.append(Position(temp[0], temp[0]))

		if self.Tibot is not None:
			temp = self.Tibot.getPositon
			position_nos_robots.append(Position(temp[0], temp[0]))

		position_hokuyo = []
		for i in range(1,9,2):
			if arguments[i] == 0 and arguments[i+1] == 0:
				break
			position_hokuyo.append(Position(arguments[i], arguments[i+1]))

		#self.__tracking(timestamp, position_nos_robots, position_hokuyo)

		#temp testing
		self.__tracking(timestamp, position_hokuyo[0:2], position_hokuyo[2:4])

	"""
	def __estimate_pos(self, timestamp): #ennemy_pos [big, small]





		pass
	"""


	def __tracking(self, timestamp, position_nos_robots, position_hokuyo):
		#TODO traitement pour suivi des robots ici

		print("-----------------\n" + str(timestamp) +"\n"+ str(position_nos_robots) +"\n"+ str(position_hokuyo))


		if OUR_ROBOTS_VISIBLE_TOURELLE == True:
			for notre_robot in position_nos_robots:
				minDist = 10000
				minId = -1
				for i in range(len(position_hokuyo)):
					d = notre_robot.distanceSquarred(position_hokuyo[i])
					if d < minDist:
						minDist = d
						minId = i
				if minId == -1:
					continue
				position_hokuyo[i] = None

		
		big = None
		small = None
		for p in position_hokuyo:
			if p == None:
				continue
			if big != None:
				if small != None:
					break
				else:
					small = p
			else:
				big = p


		print("debug: position_hokuyo:"+str(position_hokuyo))
		self.__setFormatedPosition(big, small)


		""" 
		#for notre_robot in position_nos_robots:
		if( self.__last_data_position.length < 2 ): #debut du match
			
		else: #debut du match
			estimation = self.__estimate_pos(timestamp) 
			self.__last_data_position.unshift()
			self.__last_data_timestamp.unshift()*/
		"""

		#self.Tourelle.setFormatedPosition(position_big_enemy, position_small_enemy)
		pass

	def __setFormatedPosition(self, position_big_enemy, position_small_enemy):
		"""Cette méthode ne doit être appelé qu'avec des données formatées par data/computeHokuyoData.py"""
		print("tourelle: big:"+str(position_big_enemy)+" small:"+str(position_small_enemy))
		pass
		#TODO