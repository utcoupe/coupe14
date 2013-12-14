# -*- coding: utf-8 -*-

"""
Récupère les infos de defines.h et de defines_size.c, les defines communes pour tous les systèmes
Puis il le convertie en dictionnaires, comme ça pas besoin d'éditer plusieurs fichiers
"""

import os
import re


def parseFile(path, dico, myRe, nbGroupParse=1):
	reBegin = re.compile("\s?//DEBUTPARSE\s?")
	reFin = re.compile("\s?//FINPARSE\s?")
	definesFile = open(path)
	compteur = 0
	parse = False
	nbGroup = 0

	for line in definesFile:
		if reFin.match(line):
			parse = True

		if parse and  nbGroup == nbGroupParse:
			result = myRe.match(line)
			if result: 
				constante = result.group('constante')
				value = result.group('value')
				if value:
					compteur = int(value)
				dico[constante] = compteur
				compteur += 1

		if reBegin.match(line):
			parse = True
			nbGroup += 1

	definesFile.close()


def parseConstante(address, orders, ordersSize):
	relativePath = "../../arduino/commun/communication/"

	reEnum = re.compile("\s?(?P<constante>\w*)(\s?=\s?(?P<value>.*))?,")
	reArrayC = re.compile("\s?ordreSize\[(?P<constante>\w*)\](\s?=\s?(?P<value>.*))?;")


	parseFile(relativePath + "defines.h", address, reEnum, 1)
	parseFile(relativePath + "defines.h", orders, reEnum, 2)
	parseFile(relativePath + "defines_size.c", ordersSize, reArrayC, 1)

