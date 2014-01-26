# -*- coding: utf-8 -*-
"""
GUI minimaliste pour envoyer des commandes
"""

from communication import conversion


def gui(com):
	(address, orders, ordersSize, ordersArguments, ordersRetour) = com.getConst()

	while 1:
		#address = str(raw_input("Entre une address:\n"))
		address = 2
		arguments = []
		order = str(raw_input("Entre le nom ou le numéro d'un ordre:\n"))

		if order == 'k':# arret d'urgence
			com.sendOrderAPI(address, 'A_CLEANG', *arguments)
		if order == 'a':# arret d'urgence
			arguments = [1000, 500]
			com.sendOrderAPI(address, 'A_GOTO', *arguments)
			arguments = [1000, -500]
			com.sendOrderAPI(address, 'A_GOTO', *arguments)
			arguments = [0, 0, 0]
			com.sendOrderAPI(address, 'A_GOTOA', *arguments)
		elif order in com.orders:
			if isinstance(order, (int)):
				order = com.orders[order]

			for typeToGet in ordersArguments[order]:
				if typeToGet == 'int':
					arguments.append(int(raw_input("Entre  un int\n")))
				elif typeToGet == 'float':
					arguments.append(float(raw_input("Entre un float\n")))
				elif typeToGet == 'long':
					arguments.append(long(raw_input("Entre  un long\n")))
				else:
					print "ERREUR: Parseur: le parseur a trouvé un type non supporté"
			com.sendOrderAPI(address, order, *arguments)	
		else:
			print "L'ordre n'a pas été trouvé dans les fichiers arduino"
