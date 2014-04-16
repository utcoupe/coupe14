__author__ = 'furmi'

import sys
import os
import time
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "ia"))

from comSimu import Communication
from hokuyo import Hokuyo
import threading
from multiprocessing import Process, Pipe
from define import *
import test
import main

class ProcessIA():
	"""
	Classe qui va lancer une IA en subprocess.
	"""
	def __init__(self, liste_robots):
		self.__color = liste_robots[0]
		self.__bigrobot = liste_robots[1]
		self.__minirobot = liste_robots[2]
		self.__robots = liste_robots
		self.__hokuyo = Hokuyo(self.__robots[1:])
		self.__communication = Communication(self.__bigrobot, self.__minirobot, self.__hokuyo, self)
		#communication de data entre l'IA et le simu
		self.__parent_conn, self.__child_conn = Pipe()
		#TODO lancer l'IA
		self.__process = Process(target=main.startIa, args=(self.__child_conn,self.__color))
		self.__process.start()
		time.sleep(0.1)
		#on démarre le thread de lecture des données IA renvoyées à travers le pipe
		self.__read_thread = threading.Thread(target=self.__readPipe)
		self.__read_thread.start()

	def writePipe(self, addresse, ordre, args):
		"""
		Envoie des données à l'IA à travers le Pipe
		"""
		self.__parent_conn.send((addresse, ordre, args))

	def __readPipe(self):
		"""
		Méthode de lecture des données envoyées par l'IA via le pipe.
		recv est bloquant, donc lancé dans un thread
		"""
		while True:
			if self.__parent_conn.poll(1.0):
				try:
					message = self.__parent_conn.recv()
					self.__parseDataIa(message)
				except EOFError:
					print("ERREUR: except EOFError sur recv()")



	def __parseDataIa(self, data):
		"""
		Formate les données IA reçues pour les adapter à la méthode
		sendOrderAPI de Communication
		"""
		self.__communication.orderBalancing(data[0],data[1],data[2])