# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""

from .dataStructure import *
from constantes import *
import logging



class Tourelle():
	def __init__(self, Flussmittel, Tibot, BigEnemyBot, SmallEnemyBot, communication, arduinoConstantes, address):
		self.Flussmittel = Flussmittel
		self.Tibot = Tibot
		self.BigEnemyBot = BigEnemyBot
		self.SmallEnemyBot = SmallEnemyBot
		self.__communication = communication
		self.__address = address
		self.__logger = logging.getLogger(__name__)

		self.__logger.info("Starting")

		#Variables
		self.__old_data = []
		
	"""
	def getLastDataPosition(self):
		return self.__old_data[len(self.__old_data)-1][1]
	"""

	def majPositionHokuyo(self, arguments):
		#print("debug:arguments"+str(arguments)+"\n")
		timestamp = arguments[0]

		position_nos_robots = []
		if self.Flussmittel is not None:
			temp = self.Flussmittel.getPosition()
			position_nos_robots.append(Position(temp[0], temp[1]))

		if self.Tibot is not None:
			temp = self.Tibot.getPosition()
			position_nos_robots.append(Position(temp[0], temp[1]))

		position_hokuyo = []
		for i in range(1,9,2):
			if arguments[i] == 0 and arguments[i+1] == 0:
				break
			position_hokuyo.append(Position(arguments[i], arguments[i+1]))

		#self.__tracking(timestamp, position_nos_robots, position_hokuyo)

		#temp testing
		self.__tracking(timestamp, position_hokuyo[0:2], position_hokuyo[2:4])

	
	def __estimate_pos(self): 
		
		nRobots = len(self.__old_data[0][1])

		#print("DEBUG:nRobots:"+str(nRobots))
		#print("DEBUG:__old_data"+str(self.__old_data))

		coeff = TOURELLE_PULL_PERIODE / (self.__old_data[-1][0] - self.__old_data[-2][0])
		#print("DEBUG:coeff"+str(coeff))

		def predict(pos):
			offset = pos[0].subtract(pos[1]).multiply(-coeff)
			self.__logger.info("offset:"+str(offset))
			self.__logger.info("speed:"+str(Position(offset).multiply(1/TOURELLE_PULL_PERIODE)))
			return pos[1].add(offset)

		newpos = list( map(predict, zip(self.__old_data[-2][1], self.__old_data[-1][1])))

		self.__old_data.append( (self.__old_data[-2][0], newpos) )
		pass
	


	def __tracking(self, timestamp, position_nos_robots, position_hokuyo):
		#TODO traitement pour suivi des robots ici

		#print("-----------------\n" + str(timestamp) +"\n"+ str(position_nos_robots) +"\n"+ str(position_hokuyo))


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

		predict = None
		if len(self.__old_data) >= 3:
			predict = True
			self.__old_data.pop(0)
			self.__old_data.pop(-1)

		self.__old_data.append( (timestamp, [big, small]) )
		self.__logger.info("real:     \tbig:"+str(big)+"\tsmall:"+str(small))

		if predict:
			self.__estimate_pos()

		#print("DEBUG:__old_data:"+str(self.__old_data))
		#print("debug:__old_data[-1]:"+str(self.__old_data[-1]))
		#print("debug:__old_data[-1][1]:"+str(self.__old_data[-1][1]))
		self.__setFormatedPosition(self.__old_data[-1][1][0], self.__old_data[-1][1][1])


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
		self.__logger.info("predicted:\tbig:"+str(position_big_enemy)+"\tsmall:"+str(position_small_enemy))
		pass
		#TODO