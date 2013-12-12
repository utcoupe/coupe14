# -*- coding: utf-8 -*-

"""
Récupère les infos du protocoleCodes.h, le define commun pour tous les systèmes
Puis il le convertie en un dictionnaire, comme ça pas besoin d'éditer plusieurs fichiers
"""

import os
import re

protocole = {}

SERVER_ROOT_DIR  = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(SERVER_ROOT_DIR,"protocoleCodes.h"))

for line in f:
	t = re.match('^#define\s*(?P<name>\S+)\s*(?P<value1>[0-9]*x[0-9]*)(\+(?P<value2>[0-9]*x[0-9]*))*', line)
	if t: 
		name =t.group('name')
		value = int(t.group('value1'),16)
		if t.group('value2'):
			value += int(t.group('value2'), 16)
		protocole[name] = value

f.close()

print(protocole)
