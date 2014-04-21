__author__ = 'furmi'

from define import *
import time
import math

def testIa(conn, color):
	"""
	self.__color = self.__bigrobot.getTeam()
	if self.__color == RED:
		conn.send((ADDR_TIBOT_ASSERV,A_GOTO,49,2000,400))
	elif self.__color == YELLOW:
		conn.send((ADDR_TIBOT_ASSERV,A_GOTO,36,1000,800))
	"""
	time.sleep(1)
	"""conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GOTO",(36,800,700)))
	time.sleep(3)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_GET_TRIANGLE", (50,123)))
	time.sleep(2)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_RET_OUVRIR", (54,1)))"""
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GET_POS", (53,)))
	time.sleep(2)
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_SET_POS", (54,1500,1750,math.radians(75))))
	time.sleep(2)
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GET_POS", (55,)))

	def __repr__(self):
		return "testIA"