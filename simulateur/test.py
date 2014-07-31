__author__ = 'furmi'

from define import *
import time
import math

def testIa(conn, color):
	"""
	Méthode de test très basique.
	Permet d'envoyer des ordres au simulateur via le pipe pour les tester.
	Respecter la structure :
		conn.send((adress,ordre,args))
	Avec adress, ordre et args au format texte (avec "").
	"""
	time.sleep(1)
	"""conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GOTO",(36,800,700)))
	time.sleep(3)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_GET_TRIANGLE", (50,123)))
	time.sleep(2)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_RET_OUVRIR", (54,1)))
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GET_POS", (53,)))
	time.sleep(2)
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_SET_POS", (1500,1750,math.radians(75))))
	time.sleep(2)
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GET_POS", (55,)))
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_SET_POS", (1500,1750,math.radians(0))))
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GOTO",(36,1000,800)))
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_ROT", (54,math.radians(90))))
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GOTO",(36,1100,300)))
	#conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_PWM", (54,128,128,800)))"""
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_SET_POS", (1850,900,math.radians(0))))
	time.sleep(1)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_GET_TRIANGLE", (50,)))
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_SET_POS", (1850,900,math.radians(0))))
	time.sleep(1)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_GET_TRIANGLE", (51,)))
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_SET_POS", (1850,900,math.radians(0))))
	time.sleep(1)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_GET_TRIANGLE", (52,)))
	"""time.sleep(1)
	#conn.send(("ADDR_TIBOT_OTHER","O_BALAI", (50,-1)))
	conn.send(("ADDR_TIBOT_ASSERV","A_GOTO", (13,2400,900)))"""

	def __repr__(self):
		return "testIA"