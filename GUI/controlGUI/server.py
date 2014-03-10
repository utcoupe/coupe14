# -*- coding: utf-8 -*-

import sys
sys.path.append('../../ia/')

import communication
from socket import *
import time
import threading

myHost = ''
myPort = 2001

#init comm
com = communication.CommunicationGlobale()
sock = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
sock.bind((myHost, myPort))            # bind it to the server port
sock.listen(5)                         # allow 5 simultaneous


def update():
	if len(sys.argv) == 2:
		addr = sys.argv[1]
	else:
		addr = 2
	print("Position update on adress " + str(addr))
	while 1:
		com.sendOrderAPI(addr, 'A_GET_POS')
		ret = -1
		while ret == -1:
			ret = com.readOrdersAPI(addr)
		data = ":".join(str(el) for el in ret[2])
		print(data)
		connection.send(bytes(data, 'utf-8'))
		time.sleep(0.1)


while 1:
	# wait for next client to connect
	print("Ready, waiting for socket connection")
	global connection
	global address
	connection, address = sock.accept()   # connection is a new socket
	print("Connection established")
	threading.Thread(target=update).start()
	while 1:
		data_rec = connection.recv(1024)  # receive up to 1K bytes
		if data_rec:
			data_rec = [data.split(':') for data in str(data_rec, 'utf-8').split('!')[:-1]] #conversion chaine en liste
			for data in data_rec:
				data[0] = int(data[0])
				#conversion data
				if data[1] == 'A_GOTOA': #deux int  un float
					data[2] = int(data[2])
					data[3] = int(data[3])
					data[4] = float(data[4])
				elif data[1] == 'A_PIDA' or data[1] == 'A_PIDD' or data[1] == 'A_ROT' or data[1] == 'A_ACCMAX': #all float
					for i in range(2,len(data)):
						data[i] = float(data[i])
				elif data[1] == 'A_GOTO': #all int
					for i in range(2,len(data)):
						data[i] = int(data[i])
				if data[1] == 'A_GOTO' or data[1] == 'A_GOTOA' or data[1] == 'A_ROT':
					data.insert(2, 0) #ajout id
				
				print('Data : ' + str(data))
				com.sendOrderAPI(data[0], data[1], *data[2:]) 
		else:
			break
	connection.close()              # close socket
