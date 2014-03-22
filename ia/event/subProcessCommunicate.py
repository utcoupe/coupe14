# -*- coding: utf-8 -*-
"""
Cette classe permet de communiquer avec le subprocess de choix d'objectif
"""

import threading
from multiprocessing import Process, Pipe
import logging
from collections import deque


from . import goals

class SubProcessCommunicate():
	def __init__(self, Data):
		self.__Data = Data
		self.__logger = logging.getLogger(__name__.split('.')[0])
		
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel = process(self.__Data)
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot = process(self.__Data)

		
	def readOrders(self):
		"""retourn les données des subprocess"""
		data = self.__dataToDico()
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("data", data)) #TODO: ça n'a rien à faire ici !
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("data", data))#TODO: ça n'a rien à faire ici !

		input_list_1 = deque()
		if self.__Data.Flussmittel is not None:
			input_list_1 = self.subprocess_1.readPacket()
		if self.__Data.Tibot is not None:
			input_list_2 = self.subprocess_2.readPacket()
			for info in input_list_2:
				input_list_1.append(info)

		return input_list_1

	def sendObjectifOver(self, id_objectif):
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("over", id_objectif))
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("over", id_objectif))

	def sendObjectifCanceled(self, id_objectifs_canceled):
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("over", id_objectif))
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("over", id_objectif))

	def __dataToDico(self):
		data = {}

		if self.__Data.Flussmittel is not None:
			system = self.__Data.Flussmittel
			data["Flussmittel"] = {}
			data["Flussmittel"]["getPositon"] = system.getPosition()
		else:
			data["Flussmittel"] = None

		if self.__Data.Tibot is not None:
			system = self.__Data.Tibot
			data["Tibot"] = {}
			data["Tibot"]["getPositon"] = system.getPosition()
		else:
			data["Tibot"] = None

		if self.__Data.Tourelle is not None:
			system = self.__Data.Tourelle
			data["Tourelle"] = {}
		else:
			data["Tourelle"] = None

		if self.__Data.SmallEnemyBot is not None:
			system = self.__Data.SmallEnemyBot
			data["SmallEnemyBot"] = {}
			data["SmallEnemyBot"]["getPositon"] = system.getPosition()
		else:
			data["SmallEnemyBot"] = None

		if self.__Data.BigEnemyBot is not None:
			system = self.__Data.BigEnemyBot
			data["BigEnemyBot"] = {}
			data["BigEnemyBot"]["getPositon"] = system.getPosition()
		else:
			data["BigEnemyBot"] = None

		return data

	

class process():
	def __init__(self, Data):
		self.__Data = Data
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__input_buffer = deque()

		self.__parent_conn, self.__child_conn = Pipe()
		self.__process = Process(target=goals.startSubprocess, args=(self.__child_conn,))
		self.__process.start()

		self.__Pull_thread = threading.Thread(target=self.__readPipe)
		self.__Pull_thread.start()
		

		
	def readPacket(self):
		if self.__input_buffer:
			return self.__input_buffer.popleft()
		else:
			return self.__input_buffer

	def sendPacket(self, packet):
		self.__parent_conn.send(packet)

	def __readPipe(self):
		while True:
			self.__input_buffer.append(self.__parent_conn.recv())

