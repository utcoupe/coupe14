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
		self.__input_buffer = deque()

		self.__parent_conn, self.__child_conn = Pipe()
		self.__process = Process(target=goals.startSubprocess, args=(self.__child_conn,))
		self.__process.start()

		self.__Pull_thread = threading.Thread(target=self.__manager)
		self.__Pull_thread.start()
		

		
	def readBuffer(self):
		self.__updateData() #TODO: ça n'a rien à faire ici !

		if self.__input_buffer:
			return self.__input_buffer.popleft()
		else:
			return self.__input_buffer

	def sendObjectifOver(self, id_objectif):
		self.__parent_conn.send(("over", id_objectif))

	def sendObjectifCanceled(self, id_objectifs_canceled):
		self.__parent_conn.send(("canceled", id_objectif))

	def __manager(self):
		self.__readPipe()

	def __readPipe(self):
		self.__input_buffer.append(self.__parent_conn.recv())

	def __updateData(self):
		data = {}

		if self.__Data.Flussmittel is not None:
			system = self.__Data.Flussmittel
			data["Flussmittel"] = {}
			data["Flussmittel"]["getPositon"] = system.getPositon()
		else:
			data["Flussmittel"] = None

		if self.__Data.Tibot is not None:
			data["Tibot"] = {}
			data["Tibot"]["getPositon"] = system.getPositon()
		else:
			data["Tibot"] = None

		if self.__Data.Tourelle is not None:
			data["Tourelle"] = {}
		else:
			data["Tourelle"] = None

		if self.__Data.SmallEnemyBot is not None:
			data["SmallEnemyBot"] = {}
			data["SmallEnemyBot"]["getPositon"] = system.getPositon()
		else:
			data["SmallEnemyBot"] = None

		if self.__Data.BigEnemyBot is not None:
			data["BigEnemyBot"] = {}
			data["BigEnemyBot"]["getPositon"] = system.getPositon()
		else:
			data["BigEnemyBot"] = None

		self.__parent_conn.send(("data", data))
