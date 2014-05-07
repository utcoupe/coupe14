# -*- coding: utf-8 -*-
"""
GUI minimaliste pour envoyer des commandes
"""

import time


def gui(com):
	dic = com.getConst()
	ordersArguments = dic['ordersArguments']
	arguments = []

	while 1:
		try:
			#address = str(raw_input("Entre une address:\n"))
			address = 4
			arguments = []
			order = str(input("Entre le nom ou le numéro d'un ordre:\n"))
			if order:
				if order[0] == 'A':
					address = 5
				elif order[0] == 'O':
					address = 4
				elif order == 'GET_HOKUYO':
					address = 6

				if order == 'k':# arret d'urgence
					com.sendOrderAPI(5, 'A_CLEANG', *arguments)
				elif order == 'a':# arret d'urgence
					arguments = [1000, 500]
					com.sendOrderAPI(2, 'A_GOTO', *arguments)
					arguments = [1000, -500]
					com.sendOrderAPI(2, 'A_GOTO', *arguments)
					arguments = [0, 0, 0]
					com.sendOrderAPI(2, 'A_GOTOA', *arguments)
				elif order == 'c':
					com.sendOrderAPI(5, 'A_GET_CODER', *arguments)
				elif order == 'p':
					com.sendOrderAPI(5, 'A_GET_POS', *arguments)
				elif order == 'r':
					com.sendOrderAPI(5, 'A_RESET_POS', *arguments)

				elif order == 's':

					for a in range(1000):
						arguments = []


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
		except:
			pass
