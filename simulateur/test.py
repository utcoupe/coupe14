__author__ = 'furmi'

from define import *
import time

def testIa(conn, color):
	"""
	self.__color = self.__bigrobot.getTeam()
	if self.__color == RED:
		conn.send((ADDR_TIBOT_ASSERV,A_GOTO,49,2000,400))
	elif self.__color == YELLOW:
		conn.send((ADDR_TIBOT_ASSERV,A_GOTO,36,1000,800))
	"""
	print('dans le testIa')
	time.sleep(1)
	conn.send(("ADDR_FLUSSMITTEL_ASSERV","A_GOTO",(36,800,700)))
	time.sleep(3)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_GET_TRIANGLE", (50,123)))
	time.sleep(2)
	conn.send(("ADDR_FLUSSMITTEL_OTHER","O_RET_OUVRIR", (54,1)))

	def __repr__(self):
		return "testIA"