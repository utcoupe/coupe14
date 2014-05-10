# -*- coding: utf-8 -*-
"""
Classe pour les données hokuyo
"""

from .dataStructure import *
from constantes import *
import logging
import copy



class Tourelle():
	def __init__(self, Flussmittel, Tibot, BigEnemyBot, SmallEnemyBot, MetaData, communication, arduinoConstantes, address):
		self.Flussmittel = Flussmittel
		self.Tibot = Tibot
		self.BigEnemyBot = BigEnemyBot
		self.SmallEnemyBot = SmallEnemyBot
		self.MetaData = MetaData
		self.__communication = communication
		self.__address = address
		self.__logger = logging.getLogger(__name__)

		#Variables
		self.__old_data = []
		
	"""
	def getLastDataPosition(self):
		return self.__old_data[len(self.__old_data)-1][1]
	"""

	def majPositionHokuyo(self, arguments):
		timestamp = arguments[0]
		position_hokuyo = []

		for i in range(1,9,2):
			if arguments[i] == 0 and arguments[i+1] == 0:
				break
			position_hokuyo.append(Position(arguments[i], arguments[i+1]))

		position_enemy = self.__fitreNosRobots(position_hokuyo) 
		if position_enemy != None:
			if len(position_enemy) == NUMBER_OF_ENEMY:
				i = 0
				if self.BigEnemyBot is not None:
					self.BigEnemyBot.setPosition(position_enemy[i])
					i += 1
				if self.SmallEnemyBot is not None:
					self.SmallEnemyBot.setPosition(position_enemy[i])
					i += 1
			else:
				self.__logger.warning("On a trouvé qu'un seul robot adverse dans les données hokuyo, du coup on les drop.")
		else:
			self.__logger.warning("On a trouvé aucun enemy donc on drop les données hokuyo.")
		


	def __fitreNosRobots(self, position_hokuyo):
		"""return une liste de robots ennemies, il peut manquer un robots, si il n'y en a aucun on return None"""
		position_hokuyo_base = copy.deepcopy(position_hokuyo)

		#On essaie de supprimer les robots qui corespondent aux notres et aux indications des constantes
		self.__tryRemoveOurBot(position_hokuyo, OUR_ROBOTS_VISIBLE_TOURELLE, DISTANCE_MAX_ROBOT_FUSION)
		if len(position_hokuyo) > NUMBER_OF_ENEMY:
			#cas ou ont verrai quand même nos robots
			self.__logger.warning("Attention on bypass les indications des constantes pour supprimer nos robots des données hokuyo")
			position_hokuyo = copy.deepcopy(position_hokuyo_base)
			self.__tryRemoveOurBot(position_hokuyo, True, DISTANCE_MAX_ROBOT_FUSION)
			if len(position_hokuyo) > NUMBER_OF_ENEMY:
				self.__logger.warning("Attention on va chercher nos robots plus loin que ce qui est prévu")
				position_hokuyo = copy.deepcopy(position_hokuyo_base)
				self.__tryRemoveOurBot(position_hokuyo, OUR_ROBOTS_VISIBLE_TOURELLE, float("inf"))
				self.__logger.error("Il y a un probleme avec le nombre de robots détecté par les hokuyo position_hokuyo: "+str(position_hokuyo))
			if len(position_hokuyo) > NUMBER_OF_ENEMY:
				self.__logger.error("OH ! Faut pas pousser mémé dans les begonias !")
				return None

		if len(position_hokuyo) < NUMBER_OF_ENEMY:
			self.__logger.warning("On a perdu au moins un des robots adverses position_hokuyo "+str(position_hokuyo))
		return position_hokuyo

	def __tryRemoveOurBot(self, position_hokuyo, nos_robots_visible, threshold):
		position_nos_robots = []
		if self.Flussmittel is not None:
			temp = self.Flussmittel.getPosition()
			position_nos_robots.append(Position(temp[0], temp[1]))

		if self.Tibot is not None:
			temp = self.Tibot.getPosition()
			position_nos_robots.append(Position(temp[0], temp[1]))

		if nos_robots_visible == True:
			for position_notre_robot in position_nos_robots:
				min_distance = float("inf")
				min_id = None
				for i in range(len(position_hokuyo)):
					distance = position_notre_robot.distanceSquarred(position_hokuyo[i])
					if distance < min_distance:
						min_distance = distance
						min_id = i
				if min_distance > DISTANCE_MAX_ROBOT_FUSION:
					self.__logger.warning("Nous n'avons pas trouvé un de nos robots à un emplacement proche de celui attendu min_distance: "+str(min_distance)+" position_nos_robots "+str(position_nos_robots)+" position_hokuyo: "+str(position_hokuyo))
				else:
					del position_hokuyo[min_id]

	
	def __setFormatedPosition(self, position_big_enemy, position_small_enemy):
		"""Cette méthode ne doit être appelé qu'avec des données formatées par data/computeHokuyoData.py"""
		self.SmallEnemyBot.setPosition(position_small_enemy)
		self.BigEnemyBot.setPosition(position_big_enemy)







	#Vieux code
	def __tracking(self, timestamp, position_hokuyo):

		#print("-----------------\n" + str(timestamp) +"\n"+ str(position_nos_robots) +"\n"+ str(position_hokuyo))
		
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
		#self.__logger.info("real:     \tbig:"+str(big)+"\tsmall:"+str(small))

		"""TODO fix __estimate_pos() 
		if predict: 
			self.__estimate_pos()"""

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

	def __estimate_pos(self): 
		
		nRobots = len(self.__old_data[0][1])

		#print("DEBUG:nRobots:"+str(nRobots))
		#print("DEBUG:__old_data"+str(self.__old_data))
		temp =(self.__old_data[-1][0] - self.__old_data[-2][0])
		if temp != 0:
			coeff = TOURELLE_PULL_PERIODE / temp
		else:
			coeff = 0
		#print("DEBUG:coeff"+str(coeff))

		def predict(pos):
			offset = pos[0].subtract(pos[1]).multiply(-coeff)
			#self.__logger.info("offset:"+str(offset))
			#self.__logger.info("speed:"+str(Position(offset).multiply(1/TOURELLE_PULL_PERIODE)))
			return pos[1].add(offset)

		newpos = list( map(predict, zip(self.__old_data[-2][1], self.__old_data[-1][1])))

		self.__old_data.append( (self.__old_data[-2][0], newpos) )
	