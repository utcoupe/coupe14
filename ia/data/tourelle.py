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
		self.__compteur_inversion = 0

		
	"""
	def getLastDataPosition(self):
		return self.__old_data[len(self.__old_data)-1][1]
	"""

	def majPositionHokuyo(self, arguments):
		timestamp = arguments[0]
		position_hokuyo = []

		for i in range(1,9,2):
			if arguments[i] == -1 and arguments[i+1] == -1:
				break
			position_hokuyo.append(Position(arguments[i], arguments[i+1]))

		position_enemy = self.__fitreNosRobots(position_hokuyo) 
		if position_enemy != None and len(position_enemy) > 0:
			#Si on voit les deux robots, on vérfie qu'ils ne sont pas inversés et on set
			if len(position_enemy) == 2:
				position_enemy = self.__checkRobotsPosition(position_enemy)
				if position_enemy is not None:
					i = 0
					if self.BigEnemyBot is not None:
						self.BigEnemyBot.setPosition(position_enemy[i])
						i += 1
					if self.SmallEnemyBot is not None:
						self.SmallEnemyBot.setPosition(position_enemy[i])
						i += 1
			elif NUMBER_OF_ENEMY == 1:
				self.SmallEnemyBot.setPosition(position_enemy[0])
			else:
				temp = self.BigEnemyBot.getPosition()
				ia_position_big_ennemy = Position(temp[0], temp[1])

				temp = self.SmallEnemyBot.getPosition()
				ia_position_small_ennemy = Position(temp[0], temp[1])

				if ia_position_big_ennemy.distanceSquarred(position_enemy[0]) < ia_position_small_ennemy.distanceSquarred(position_enemy[0]):
					self.BigEnemyBot.setPosition(position_enemy[0])
				else:
					self.SmallEnemyBot.setPosition(position_enemy[0])
		else:
			self.__logger.warning("On a trouvé aucun enemy donc on drop les données hokuyo.")
	
	def __checkRobotsPosition(self, position_enemy):
		temp = self.BigEnemyBot.getPosition()
		ia_position_big_ennemy = Position(temp[0], temp[1])

		temp = self.SmallEnemyBot.getPosition()
		ia_position_small_ennemy = Position(temp[0], temp[1])

		if ia_position_big_ennemy.distanceSquarred(position_enemy[0]) > ia_position_big_ennemy.distanceSquarred(position_enemy[1]) or ia_position_small_ennemy.distanceSquarred(position_enemy[1]) > ia_position_small_ennemy.distanceSquarred(position_enemy[0]):
			if self.__compteur_inversion < 3:
				self.__logger.warning("L'hokuyo semble avoir confondu le petit et le gros robots adverse ia_position_big_ennemy "+str(ia_position_big_ennemy)+" position_enemy[0] "+str(position_enemy[0])+" ia_position_small_ennemy "+str(ia_position_small_ennemy)+" position_enemy[1] "+str(position_enemy[1]))
				self.__compteur_inversion += 1
				return None
			else:
				self.__logger.warning("On accepte finalement les données hokuyo, donc on inverse la position des robots ennemy dans l'IA")
		
		self.__compteur_inversion = 0
		return position_enemy

	def __fitreNosRobots(self, position_hokuyo):
		"""return une liste de robots ennemies, il peut manquer un robots, si il n'y en a aucun on return None"""
		position_hokuyo_base = copy.deepcopy(position_hokuyo)

		#On essaie de supprimer les robots qui corespondent aux notres et aux indications des constantes
		self.__tryRemoveOurBot(position_hokuyo, OUR_ROBOTS_VISIBLE_TOURELLE, DISTANCE_MAX_ROBOT_FUSION)
		if len(position_hokuyo) > NUMBER_OF_ENEMY:
			self.__logger.warning("Attention on drop les données hokuyo, on voit trop d'objet "+str(position_hokuyo))
			return None
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
	
