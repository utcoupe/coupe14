# -*- coding: utf-8 -*-
"""
Ce fichier gère les conversion pour la communication
"""

import struct

def binaryToFloat(string):
	#convertion d'un chaine de binaire en float
	def as_float32(s):
	    """
	    See: http://en.wikipedia.org/wiki/IEEE_754-2008
	    """
	    from struct import pack,unpack
	    return unpack("f",pack("I", bits2int(s)))

	# Where the bits2int function converts bits to an integer.  
	def bits2int(bits):
	    # You may want to change ::-1 if depending on which bit is assumed
	    # to be most significant. 
	    bits = [int(x) for x in bits[::-1]]

	    x = 0
	    for i in range(len(bits)):
	        x += bits[i]*2**i
	    return x

	temp = ""
	for i in range(24, 32, 1):
		temp += string[i]
	for i in range(16, 24, 1):
		temp += string[i]
	for i in range(8, 16, 1):
		temp += string[i]
	for i in range(0, 8, 1):
		temp += string[i]

	resultat = as_float32(temp)[0]

	#TODO gérer les float négatif et tester car taille(floatArduino) != taille(floatPC)
	return resultat


def binaryToInt(string):
	temp = ""
	for i in range(8, 16, 1):
		temp += string[i]
	for i in range(0, 8, 1):
		temp += string[i]

	resultat = int(temp, 2)
	if resultat>32767:
		resultat -= 65536
	return resultat

def binaryToLong(string):
	temp = ""
	for i in range(16, 24, 1):
		temp += string[i]
	for i in range(8, 16, 1):
		temp += string[i]
	for i in range(0, 8, 1):
		temp += string[i]

	resultat = int(temp, 2)
	if resultat>2147483647: #si le nombre est négatif
		resultat -= 4294967295
	return resultat


def floatToBinary(num):
	"""retourne une chaine de 32 bits"""
	temp = ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))
	temp2 = ""
	for i in range(24, 32, 1):
		temp2 += temp[i]
	for i in range(16, 24, 1):
		temp2 += temp[i]
	for i in range(8, 16, 1):
		temp2 += temp[i]
	for i in range(0, 8, 1):
		temp2 += temp[i]

	return temp2


def longToBinary(num):
	"""retourne une chaine de 32 bits"""
	temp2 = ""
	
	if num<0: #si l'int est négatif
		num = 4294967295 + num

	temp = bin(num)[2:]

	while len(temp) < 32:
		temp = '0' + temp

	#On inverse les 16 bits par blocks de 8, exemple AAAAAAAABBBBBBBB devient BBBBBBBBAAAAAAAA
	for i in range(24, 32, 1):
		temp2 += temp[i]
	for i in range(16, 24, 1):
		temp2 += temp[i]
	for i in range(8, 16, 1):
		temp2 += temp[i]
	for i in range(0, 8, 1):
		temp2 += temp[i]
	return temp2


def intToBinary(num):
	"""retourne une chaine de 16 bits"""
	temp2 = ""
	
	if num<0: #si l'int est négatif
		num = 65536 + num

	temp = bin(num)[2:]

	while len(temp) < 16:
		temp = '0' + temp

	#On inverse les 16 bits par blocks de 8, exemple AAAAAAAABBBBBBBB devient BBBBBBBBAAAAAAAA
	for i in range(8, 16, 1):
		temp2 += temp[i]
	for i in range(0, 8, 1):
		temp2 += temp[i]
	return temp2


def orderToBinary(num):
	"""retourne une chaine de 6 bits"""
	temp = bin(num)[2:]
	while len(temp) < 6:
		temp = '0' + temp
	return temp
