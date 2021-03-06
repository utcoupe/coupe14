# -*- coding: utf-8 -*-
"""
GUI minimaliste pour envoyer des commandes
"""

import time


def gui(com):
	dic = com.getConst()
	ordersArguments = dic['ordersArguments']
	arguments = []
	last_ordre = ''
	last_arg = []

	while 1:
		try:
			#address = str(raw_input("Entre une address:\n"))
			address = 4
			arguments = []
			order = str(input("Entre le nom ou le numéro d'un ordre:\n"))
			if order:
				if order == '.':
					arguments = last_arg
					order = last_ordre
				if order[0] == 'A':
					address = 2
				elif order[0] == 'O':
					address = 1
				elif order[0] == 'T':
					address = 5
				if order == 'k':# arret d'urgence
					com.sendOrderAPI(2, 'A_CLEANG', *arguments)
				elif order == 'a':# arret d'urgence
					arguments = [0, 1000, 0]
					com.sendOrderAPI(2, 'A_GOTO', *arguments)
					arguments = [0, 0, 0, 0.0]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
				elif order == 'c':
					com.sendOrderAPI(2, 'A_GET_CODER', *arguments)
				elif order == 'p':
					com.sendOrderAPI(2, 'A_GET_POS', *arguments)
				elif order == 'r':
					arguments = [0, 0, 0.0]
					com.sendOrderAPI(2, 'A_SET_POS', *arguments)
				elif order == 't':
					arguments = []
					com.sendOrderAPI(5, 'T_GET_CAM', *arguments)
					com.sendOrderAPI(5, 'T_GET_HOKUYO', *arguments)
				elif order == 'm':
					i = 10
					while i >0:
						arguments = [9, 100, 100, 1000]
						com.sendOrderAPI(2, 'A_PWM', *arguments)
						time.sleep(4)
						arguments = [10, -100, -100, 1000]
						com.sendOrderAPI(2, 'A_PWM', *arguments)
						time.sleep(4)
						i -= 1


				elif order == 's':
					arguments = [0,2000,0]
					com.sendOrderAPI(2, 'A_GOTO', *arguments)
					arguments = [0,2300,-800]
					com.sendOrderAPI(2, 'A_GOTO', *arguments)
					arguments = [0,2000,-1000]
					com.sendOrderAPI(2, 'A_GOTO', *arguments)
					arguments = [0,1000,-1200]
					com.sendOrderAPI(2, 'A_GOTO', *arguments)
					arguments = [0,500,-900]
					com.sendOrderAPI(2, 'A_GOTO', *arguments)
					arguments = [0,0,0,0.0]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
					"""arguments = [0, 2000, 0, 3.14]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
					arguments = [0, 0, 0, 0.0]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
					arguments = [0, 2000, 0, 3.14]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
					arguments = [0, 0, 0, 0.0]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
					arguments = [0, 2000, 0, 3.14]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
					arguments = [0, 0, 0, 0.0]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
					arguments = [0, 2000, 0, 3.14]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
					arguments = [0, 0, 0, 0.0]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)"""

				elif order in com.orders:
					if isinstance(order, (int)):
						order = com.orders[order]

					for typeToGet in ordersArguments[order]:
						if typeToGet == 'int':
							arguments.append(int(input("Entre  un int\n")))
						elif typeToGet == 'float':
							arguments.append(float(input("Entre un float\n")))
						elif typeToGet == 'long':
							arguments.append(int(input("Entre  un long\n")))
						else:
							print("ERREUR: Parseur: le parseur a trouvé un type non supporté")
					com.sendOrderAPI(address, order, *arguments)	
				else:
					print("L'ordre n'a pas été trouvé dans les fichiers arduino")
			last_ordre = order
			last_arg = arguments
		except Exception as e:
			print(e)
