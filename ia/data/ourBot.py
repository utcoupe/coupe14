# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""

from collections import deque

class OurBot():
	def __init__(self, name, constantes, communication, arduinoConstantes, addressOther, addressAsserv, largeur, longueur):
		#Constantes
		self.communication = communication
		self.addressOther = addressOther
		self.addressAsserv = addressAsserv
		self.__name = name

		self.largeur = largeur 
		self.longueur = longueur


		#Valeurs récupérées (read-only)
		self.positionX = 0
		self.positionY = 0
		self.angle = 0.0

		#Variables
		self.__objectifs = None #[(id, ((id_action, action), (id_action, action), ...)), ...]

	#Getter
	def getPositon(self):
		return (self.positionX, self.positionY)

	#utilise les données en provenance de nos robots pour mettre à jour les données de la classe
	def majPosition(self, arguments):
		self.positionX = arguments[0]
		self.positionY = arguments[1]
		self.angle = arguments[2]

	def getNextIdOrder(self):
		if self.__objectifs != None:
			return (self.__objectifs[0][0], self.__objectifs[0][3][0]) #(id_objectif_0, id_action_0_de_objcetif_0)
		else:
			return None

	def getNextOrders(self):
		if self.__objectifs != None:
			objectif_en_cours = self.objectifs.popleft()
			output_finale = []
			output_finale += objectif_en_cours[0]
			order_of_objectif = objectif_en_cours[1]

			data_order = order_of_objectif.pop()
			output_temp = deque()
			output_temp.append(data_order)
			while data_order[1][0] != 'SLEEP' or data_order[1][0] != 'THEN' or data_order[1][0] != 'FIN':
				data_order = order_of_objectif.popleft()
				output_temp.append(data_order)

			if data_order[1][0] != 'FIN':
				self.__objectifs.appendleft(objectif_en_cours)

			output_finale += output_temp
			return output_finale

		else:
			return None

	def getName(self):
		return self.__name

