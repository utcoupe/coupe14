# -*- coding: utf-8 -*-

import sys
sys.path.append('../../ia/')

import communication
from socket import *

myHost = ''
myPort = 2001

#init comm
com = communication.CommunicationGlobale()
sock = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
sock.bind((myHost, myPort))            # bind it to the server port
sock.listen(5)                         # allow 5 simultaneous

while 1:
	# wait for next client to connect
	print("Ready, waiting for socket connection")
	connection, address = sock.accept() # connection is a new socket
	print("Connection established")
	while 1:
		data_rec = connection.recv(1024) # receive up to 1K bytes
		if data_rec:
			data_rec = [data.split(':') for data in str(data_rec, 'utf-8').split('!')[:-1]] #conversion chaine en liste
			for data in data_rec:
				data[0] = int(data[0])
				#conversion data
				if data[1] == 'A_GOTO': #deux int 
					for i in range(2,len(data)):
						data[i] = int(data[i])
				elif data[1] == 'A_ROT' or data[1] == 'A_ACCMAX':
					data[2] = float(data[2])
				elif data[1] == 'A_PIDA' or data[1] == 'A_PIDD':
					for i in range(2,len(data)):
						data[i] = float(data[i])
				
				print('Data : ' + str(data))
				com.sendOrderAPI(data[0], data[1], *data[2:]) 
		else:
			break
	connection.close()              # close socket
