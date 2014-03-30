__author__ = 'furmi'

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "map"))

from communication import Communication
from hokuyo import Hokuyo
import threading
from multiprocessing import Process, Pipe
from define import *
import test

class ProcessIA():
	"""
	Classe qui va lancer une IA en subprocess.
	"""
	def __init__(self, liste_robots):
		self.__bigrobot = liste_robots[0]
		self.__minirobot = liste_robots[1]
		self.__robots = liste_robots
		self.__hokuyo = Hokuyo(self.__robots)
		self.__communication = Communication(self.__bigrobot, self.__minirobot, self.__hokuyo, self)
		#communication de data entre l'IA et le simu
		self.__parent_conn, self.__child_conn = Pipe()
		#TODO lancer l'IA
		self.__process = Process(target=test.testIa, args=(self.__child_conn,))
		self.__process.start()
		#on démarre le thread de lecture des données IA renvoyées à travers le pipe
		self.__read_thread = threading.Thread(target=self.__readPipe)
		self.__read_thread.start()

	def writePipe(self, addresse, ordre, args):
		"""
		Envoie des données à l'IA à travers le Pipe
		Tourne dans un thread
		"""
		self.__parent_conn((addresse, ordre, args))

	def __readPipe(self):
		"""
		Méthode de lecture des données envoyées par l'IA via le pipe.
		recv est bloquant, donc lancé dans un thread
		"""
		while True:
			self.__parseDataIa(self.__parent_conn.recv())

	def __parseDataIa(self, data):
		"""
		Formate les données IA reçues pour les adapter à la méthode
		sendOrderAPI de Communication
		"""
		self.__communication.sendOrderAPI(data[0],data[1],data[2],data[3],data[4])