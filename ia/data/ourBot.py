# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""

from constantes import *
from math import sqrt
import logging
from collections import deque

from .idRot import *

class OurBot():
	def __init__(self, name, communication, arduinoConstantes, addressOther, addressAsserv, largeur, longueur):
		#Constantes
		self.__name = name
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__arduino_constantes = arduinoConstantes
		self.__communication = communication
		self.__addressOther = addressOther
		self.__addressAsserv = addressAsserv

		self.largeur = largeur 
		self.longueur = longueur
		self.rayon = sqrt(self.largeur * self.largeur + self.longueur * self.longueur)


		#Valeurs récupérées (read-only)
		self.__positionX = 0
		self.__positionY = 0
		self.__angle = 0.0
		self.__last_id_executed_other = ID_ACTION_MAX
		self.__last_id_executed_asserv = ID_ACTION_MAX

		self.__last_id_action_stacked = IdRot()

		#Variables
		self.__objectifs = deque() #((id, ((id_action, ordre, arguments), (id_action, ordre, arguments), ...)), ...)
		self.__actions_en_cours = None
		self.__last_id_objectif_executed = None

		#Variable pour evenManager
		self.__id_to_reach = "ANY"

	#Getter
	def getPosition(self):
		return (self.__positionX, self.__positionY)

	def getRayon(self):
		return self.rayon

	def getName(self):
		return self.__name

	def getLastIdGlobale(self):
		return self.maxRot(self.__last_id_executed_other, self.__last_id_executed_asserv)

	def getAddressOther(self):
		return self.__addressOther

	def getAddressAsserv(self):
		return self.__addressAsserv

	def getQueuedObjectif(self):
		return (self.__actions_en_cours, self.__objectifs)

	def getLastIdObjectifExecuted(self):
		return self.__last_id_objectif_executed

	def getTrajectoires(self):
		data_trajectoires = ()
		trajectoire = ((self.__positionX, self.__positionY),)

		#Pour les actions en cours d'execution
		id_action_en_cours = None
		if self.__actions_en_cours is not None:
			id_action_en_cours = self.__actions_en_cours[0]
			for order in self.__actions_en_cours[1]:
				if order[1] == 'A_GOTO':
					trajectoire += ((order[2][0], order[2][1]),)
			if not self.__objectifs:
				if len(trajectoire)>1:
					data_trajectoires += ((id_action_en_cours, trajectoire),)
					trajectoire = ()

		#Pour les objectifs prévu par la suite
		if self.__objectifs:
			id_first_action_objectif = self.__objectifs[0][0]
			#Si un objectif est à moitier en cours
			if id_action_en_cours is not None:
				if id_action_en_cours != id_first_action_objectif:
					data_trajectoires += ((id_action_en_cours, trajectoire),)
					trajectoire = ()
			
			for objectif in self.__objectifs:
				id_objectif = objectif[0]
				for order in objectif[1]:
					if order[1] == 'A_GOTO':
						trajectoire += ((order[2][0], order[2][1]),)
				if len(trajectoire)>1:
					data_trajectoires += ((id_objectif, trajectoire),)
					trajectoire = ()

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

		else:
			self.__actions_en_cours = None
		
		return self.__actions_en_cours

	def getIdToReach(self):
		return self.__id_to_reach

	def __getNextIdToStack(self):
		return self.__last_id_action_stacked.idIncrementation()

	def setIdToReach(self, id):
		self.__id_to_reach = id

	def setLastIdObjectifExecuted(self, idd):
		self.__last_id_objectif_executed = idd

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

	def addNewObjectif(self, id_objectif, action_data):
		new_objectif = (id_objectif,)
		data_objectif = deque()
		for elm_action in action_data:
			action = (self.__getNextIdToStack(),)
			order = elm_action[0]
			action += (order,)

			if order not in ("SLEEP", "THEN", "END"):
				argument_type_list = self.__arduino_constantes['ordersArguments'][order]
				arguments_temp = ()
				for i, argument_type in enumerate(argument_type_list):
					#le premier argument est l'id d'action
					if i != 0:
						if argument_type == "int":
							arguments_temp += (int(elm_action[1][i-1]),)
						elif argument_type == "float":
							arguments_temp += (float(elm_action[1][i-1]),)
						elif argument_type == "long":
							arguments_temp += (long(elm_action[1][i-1]),)

				if arguments_temp != ():
					action += (arguments_temp,)
				else:
					action += (None,)

			elif order == "SLEEP":
				arguments_temp = (int(elm_action[1][0]),)
				action += (arguments_temp,)

			else:
				action += (None,)

			data_objectif.append(action)

		self.__objectifs.append((id_objectif, data_objectif))
		self.__logger.debug( str(self.getName()) + " new goals queued: " + str((id_objectif, data_objectif)))

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

	def removeObjectifAbove(self, id_objectif):
		"""remove all queued goal on top of id_objectif, id_objectif included"""
		id_canceled_list = []

		#on vide les objectifs en cours
		if self.__actions_en_cours is not None:
			id = self.__actions_en_cours[0]
			if id_objectif == id:
				self.__actions_en_cours = None
				id_canceled_list.append(id)

		#on vide les objectifs en attente
		for objectif in self.__objectifs:
			id = objectif[0]
			if id_objectif == id:
				removed_objectif = self.__objectifs.pop()
				while removed_objectif[0] != id_objectif:
					id_canceled_list.append(removed_objectif[0])
					removed_objectif = self.__objectifs.pop()
				break

		return id_canceled_list
	

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


