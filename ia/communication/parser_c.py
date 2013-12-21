# -*- coding: utf-8 -*-

"""
Récupère les infos de defines.h et de defines_size.c, les defines communes pour tous les systèmes
Puis il le convertie en dictionnaires, comme ça pas besoin d'éditer plusieurs fichiers
"""

import os
import re


def parseFile(path, myRe, nbGroupParse=1):
	reBegin = re.compile("\s?//DEBUTPARSE\s?")
	reFin = re.compile("\s?//FINPARSE\s?")
	definesFile = open(path)
	compteur = 0
	parse = False
	nbGroup = 0
	dico = {}

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
				dico[compteur] = constante
				compteur += 1

		if reBegin.match(line):
			parse = True
			nbGroup += 1

	definesFile.close()

	return dico


def parseConstante():
	relativePath = "../../libs/com_C/"

	reEnum = re.compile("\s?(?P<constante>\w*)(\s?=\s?(?P<value>.*))?,")
	reArrayC = re.compile("\s?ordreSize\[(?P<constante>\w*)\](\s?=\s?(?P<value>.*))?;")


	address = parseFile(relativePath + "serial_defines.h", reEnum, 1)
	orders = parseFile(relativePath + "serial_defines.h", reEnum, 2)
	ordersSize = parseFile(relativePath + "serial_defines.c", reArrayC, 1)

	return (address, orders, ordersSize)
