# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""


from collections import deque
from xml.dom.minidom import parseString
from constantes import *
from math import sqrt
import logging

from .idRot import *

class OurBot():
	def __init__(self, name, communication, arduinoConstantes, addressOther, addressAsserv, largeur, longueur):
		#Constantes
		self.__name = name
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__communication = communication
		self.__addressOther = addressOther
		self.__addressAsserv = addressAsserv

		self.largeur = largeur 
		self.longueur = longueur


		#Valeurs récupérées (read-only)
		self.__positionX = 0
		self.__positionY = 0
		self.__angle = 0.0
		self.__last_id_executed_other = ID_ACTION_MAX
		self.__last_id_executed_asserv = ID_ACTION_MAX

		self.__last_id_action_stacked = IdRot()

		#Variables
		self.__objectifs = None #((id, ((id_action, ordre, arguments), (id_action, ordre, arguments), ...)), ...)
		self.__actions_en_cours = None

	#Getter
	def getPositon(self):
		return (self.__positionX, self.__positionY)

	def getName(self):
		return self.__name

	def getLastIdGlobale(self):
		return self.maxRot(self.__last_id_executed_other, self.__last_id_executed_asserv)

	def getAddressOther(self):
		return self.__addressOther

	def getAddressAsserv(self):
		return self.__addressAsserv

	def getTrajectoires(self):
		data_trajectoires = ()

		#Pour les actions en cours d'execution
		if self.__actions_en_cours is not None:
			idd = objectif[0]
			trajectoire = ((self.__positionX, self.__positionY),)
			for order in objectif[1]:
				if order[1] == 'A_GOTO':
					trajectoire += ((order[2][0]), order[2][1])
			data_objectif += (idd, trajectoire)

		#Pour les objectifs prévu par la suite
		elif self.__objectifs is not None:
			
			idd = self.__objectifs[0][0]
			trajectoire = ((self.__positionX, self.__positionY),)

			for objectif in self.__objectifs:
				for order in objectif[1]:
					if order[1] == 'A_GOTO':
						trajectoire += ((order[2][0]), order[2][1])
				data_objectif += (idd, trajectoire)

		return data_trajectoires #type: ((id_objectif, ((x,y),(x,y),...)), (id_objectif, ((x,y),(x,y),...)), ...)

	def getNextOrders(self):
		"""retourne une liste d'action qui s'arrete sur le premier ordre bloquant trouvé (END,THEN ou SLEEP) """
		if self.__objectifs:
			objectif_en_cours = self.__objectifs.popleft()
			order_of_objectif = objectif_en_cours[1] # type ((id_action, ordre, arguments),...)

			data_order = order_of_objectif.popleft() #type (id_action, ordre, arguments)
			output_temp = deque()
			output_temp.append(data_order)
			while data_order[1] != 'SLEEP' and data_order[1] != 'THEN' and data_order[1] != 'END':
				data_order = order_of_objectif.popleft()
				output_temp.append(data_order)

			if data_order[1] != 'END':
				self.__objectifs.appendleft(objectif_en_cours)

			self.__actions_en_cours = (objectif_en_cours[0], output_temp)# type (id_objectif, (data_order1, data_order2, ...)
			return  self.__actions_en_cours

		else:
			self.__actions_en_cours = None
			return None

	def __getNextIdToStack(self):
		return self.__last_id_action_stacked.idIncrementation()

	def setLastId(self, address, idd):
		if address == 'ADDR_FLUSSMITTEL_OTHER' or address == 'ADDR_TIBOT_OTHER':
			if idd != self.__last_id_executed_other:
				self.__last_id_executed_other = idd
				self.__logger.debug("changement d'id other " + str(idd))
		else:
			if idd != self.__last_id_executed_asserv:
				self.__last_id_executed_asserv = idd
				self.__logger.debug("changement d'id asserv " + str(idd))

	#utilise les données en provenance de de l'asserv uniquement !
	def setPositionAndId(self, address, arguments):
		self.positionX = arguments[0]
		self.positionY = arguments[1]
		self.angle = arguments[2]
		self.setLastId(address, arguments[3])

	def removeActionBellow(self, lastIddExecuted):
		"""enleve les actions terminé de la liste des actions en cours """
		if self.__actions_en_cours is not None:
			order_of_objectif = self.__actions_en_cours[1] # il ne peut y avoir qu'un objectif à la fois
			if order_of_objectif:
				data_order = order_of_objectif.popleft() #type (id_action, ordre, arguments)
				
				while (self.maxRot(data_order[0], lastIddExecuted) == lastIddExecuted) and order_of_objectif:
					data_order = order_of_objectif.popleft()

				if not order_of_objectif:
					self.__actions_en_cours = None


	def loadActionScript(self, filename):
		self.__logger.info(str(self.__name) + ": loading actionScript from: " + str(filename))
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()

		objectif = deque()
		for xml_goal in dom.getElementsByTagName('objectif'):
			objectif_name	= xml_goal.attributes["objectif_name"].value #seulement pour information
			id_objectif		= xml_goal.getElementsByTagName('idd')[0].firstChild.nodeValue

			data_objectif = deque()
			for xml_execution in xml_goal.getElementsByTagName('action'):
				action 		= (self.__getNextIdToStack(),)
				ordre 		= (xml_execution.getElementsByTagName('ordre')[0].firstChild.nodeValue,)
				action += ordre

				if ordre[0] == 'A_ROT':
					arguments = xml_execution.getElementsByTagName('arguments')[0].firstChild
					if arguments:
						action 		+= (list(map(float, arguments.nodeValue.split(','))),)
					else:
						action += (None,)
				else:
					arguments = xml_execution.getElementsByTagName('arguments')[0].firstChild
					if arguments:
						action 		+= (list(map(int, arguments.nodeValue.split(','))),)
					else:
						action += (None,)

				data_objectif.append(action)

			objectif.append((id_objectif, data_objectif))

		self.__objectifs = objectif
		self.__logger.debug("Script de " + str(self.__name) + "chargé: " + str(self.__objectifs))
	

	def maxRot(self, id1, id2):
		"""Retourne le plus grand id rotationnelle"""
		if id1 > id2:
			if (id1 - id2) < ID_ACTION_MAX/2:
				return id1
			else:
				return id2
		else:
			if (id2 - id1) < ID_ACTION_MAX/2:
				return id2
			else:
				return id1


