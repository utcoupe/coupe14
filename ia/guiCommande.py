# -*- coding: utf-8 -*-
"""
GUI minimaliste pour envoyer des commandes
"""

from communication import conversion


def gui(com):
	(address, orders, ordersSize, ordersArguments, ordersRetour) = com.getConst()

	while 1:
		dataString = str(raw_input("Entre le nom ou le numéro d'un ordre:\n"))
		address = 2

		if dataString == 'k':# arret d'urgence
			com.sendOrder(orders['A_KILLG'], (address, conversion.orderToBinary(int(orders['A_KILLG']))))	
		elif dataString in orders:
			ordre = int(orders[dataString])
			data = conversion.orderToBinary(ordre)

			if dataString[0] == 'A':
				address = 2
			elif dataString[0] == 'O':
				address = 1
			else:
				address = int(raw_input("Entrez adresse :"))

			for typeToGet in ordersArguments[dataString]:
				if typeToGet == 'int':
					data += conversion.intToBinary(int(raw_input("Entre  un int\n")))
				elif typeToGet == 'float':
					data += conversion.floatToBinary(float(raw_input("Entre un float\n")))
				elif typeToGet == 'long':
					data += conversion.intToBinary(long(raw_input("Entre  un long\n")))
				else:
					print "ERREUR: Parseur: le parseur a trouvé un type non supporté"
			com.sendOrder(ordre, (address,data))	
		else:
			print "L'ordre n'a pas été trouvé dans les fichiers arduino"
