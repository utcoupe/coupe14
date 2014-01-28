# -*- coding: utf-8 -*-
"""
GUI minimaliste pour envoyer des commandes
"""

from communication import conversion
import time


def gui(com):
	(address, orders, ordersSize, ordersArguments, ordersRetour) = com.getConst()
	arguments = []

	while 1:
		#address = str(raw_input("Entre une address:\n"))
		address = 3
		arguments = []
		order = str(input("Entre le nom ou le numéro d'un ordre:\n"))
		if order:
			if order[0] == 'A':
				address = 2
			elif order[0] == 'O':
				address = 1

			if order == 'k':# arret d'urgence
				com.sendOrderAPI(2, 'A_CLEANG', *arguments)
			elif order == 'a':# arret d'urgence
				arguments = [1000, 500]
				com.sendOrderAPI(2, 'A_GOTO', *arguments)
				arguments = [1000, -500]
				com.sendOrderAPI(2, 'A_GOTO', *arguments)
				arguments = [0, 0, 0]
				com.sendOrderAPI(2, 'A_GOTOA', *arguments)
			elif order == 's':

				for a in range(100):
					arguments = []
					com.sendOrderAPI(2, 'PINGPING_AUTO', *arguments)
					com.sendOrderAPI(2, 'PINGPING_AUTO', *arguments)
					com.sendOrderAPI(2, 'PINGPING_AUTO', *arguments)
					com.sendOrderAPI(2, 'PINGPING_AUTO', *arguments)
					com.sendOrderAPI(2, 'A_GET_CODER', *arguments)
					com.sendOrderAPI(2, 'A_GET_CODER', *arguments)
					com.sendOrderAPI(2, 'A_GET_CODER', *arguments)
					com.sendOrderAPI(2, 'A_GET_CODER', *arguments)

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
