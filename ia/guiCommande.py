# -*- coding: utf-8 -*-
"""
GUI minimaliste pour envoyer des commandes
"""

from communication import conversion


def gui(com):
	(address, orders, ordersSize, ordersArguments, ordersRetour) = com.getConst()

	while 1:
		dataString = str(raw_input("Entre le nom ou le numéro d'un ordre: "))
		address = 2

		if dataString == 'k':# arret d'urgence
			com.sendOrder(ordre, (address, orderToBinary(int(orders['A_KILLG']))))	
		elif dataString in orders:
			ordre = int(orders[dataString])
			data = conversion.orderToBinary(ordre)

			for typeToGet in ordersArguments[dataString]:
				if typeToGet == 'int':
					data += conversion.intToBinary(int(raw_input("Entre  un int ")))
				elif typeToGet == 'float':
					data += conversion.floatToBinary(float(raw_input("Entre un float ")))
				elif typeToGet == 'long':
					data += conversion.intToBinary(long(raw_input("Entre  un long ")))
				else:
					print("\nERREUR: Parseur: le parseur a trouvé un type non supporté")
			com.sendOrder(ordre, (address,data))	
		else:
			print ("\nL'ordre n'a pas été trouvé dans les fichiers arduino")
