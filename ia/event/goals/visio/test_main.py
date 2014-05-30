#!/usr/bin/env python3

import sys
import time
import os

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR,"../../../"))
from visio import Visio

try:
	index = sys.argv[1]
except:
	index = 0

robot = {}
robot["getPosition"] = (300,100)
robot["getPositionAndAngle"] = (300,100,0.0)

v = Visio('../../../../supervisio/visio', index, '../../../../config/visio/visio_robot/', robot, False)
#v2 = Visio('../../../../supervisio/visio', index+1, '../../../../config/visio/visio_tourelle_red/', None, False)
print('Visio started')

while 1:
	start = time.time()
	tris = v.update()
	#tris = v2.update()
	print("Duration : ", time.time() - start)
	for tri in tris:
		print(tri)
	print()
	time.sleep(1/30)
