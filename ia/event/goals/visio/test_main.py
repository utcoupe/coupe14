#!/usr/bin/env python3

from visio import Visio
import sys
import time

try:
	index = sys.argv[1]
except:
	index = 0

v = Visio('../../../../supervisio/visio', index, '../../../../config/visio/visio_robot/', None, False)
#v2 = Visio('../../../../supervisio/visio', index+1, '../../../../config/visio/visio_tourelle_red/', None, False)
print('Visio started')

while 1:
	start = time.time()
	tris = v.update(True)
	#tris = v2.update()
	print("Duration : ", time.time() - start)
	for tri in tris:
		print(tri)
	print()
	time.sleep(1)
