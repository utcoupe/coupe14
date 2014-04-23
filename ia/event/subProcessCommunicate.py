# -*- coding: utf-8 -*-
"""
Cette classe permet de communiquer avec le subprocess de choix d'objectif
"""

import threading
from multiprocessing import Process, Pipe
import logging
from collections import deque
import time


from . import goals

class SubProcessCommunicate():
	def __init__(self, Data):
		self.__Data = Data
		self.__logger = logging.getLogger(__name__.split('.')[0])
		
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel = MyProcess(self.__Data, self.__Data.Flussmittel.getName())
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot = MyProcess(self.__Data, self.__Data.Tibot.getName())

		time.sleep(0.1)
		
	def readOrders(self):
		"""retourne les données des subprocess"""
		data = self.__Data.dataToDico()
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("data", data)) #TODO: ça n'a rien à faire ici !
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("data", data))#TODO: ça n'a rien à faire ici !

		input_list = deque()
		if self.__Data.Flussmittel is not None:
			input_list.extend(self.__subprocess_flussmittel.readPackets())
		if self.__Data.Tibot is not None:
			input_list.extend(self.__subprocess_tibot.readPackets())

		return input_list

	def sendObjectifOver(self, id_objectif):
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("END", id_objectif))
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("END", id_objectif))

	def sendObjectifStepOver(self, id_objectif):
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("STEP_OVER", id_objectif))
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("STEP_OVER", id_objectif))

	def sendObjectifDynamiqueOver(self, id_objectif):
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("DYNAMIQUE_OVER", id_objectif))
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("DYNAMIQUE_OVER", id_objectif))

	def sendObjectifsCanceled(self, id_canceled_list):
		if self.__Data.Flussmittel is not None:
			for id_canceled in id_canceled_list:
				self.__subprocess_flussmittel.sendPacket(("CANCELED", id_canceled))
		if self.__Data.Tibot is not None:
			for id_canceled in id_canceled_list:
				self.__subprocess_tibot.sendPacket(("CANCELED", id_canceled))

	def sendBrasStatus(self, etat, id_objectif):
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("BRAS_STATUS", etat, id_objectif))
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("BRAS_STATUS", etat, id_objectif))

class MyProcess():
	def __init__(self, Data, robot_name):
		self.__Data = Data
		self.__logger = logging.getLogger(__name__.split('.')[0])

		self.__parent_conn, self.__child_conn = Pipe()
		self.__process = Process(target=goals.startSubprocess, args=(self.__child_conn, robot_name) )
		self.__process.start()
	
	def readPackets(self):
		new_data = deque()
		try:
			while self.__parent_conn.poll():
				new_data.append(self.__parent_conn.recv())
		except EOFError:
			self.__logger.error("except EOFError sur recv()")

		return new_data

	def sendPacket(self, packet):
		self.__parent_conn.send(packet)

		

