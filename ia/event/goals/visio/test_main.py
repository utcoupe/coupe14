#!/usr/bin/env python3

from visio import Visio
import sys
import time

try:
	index = sys.argv[1]
except:
	index = 0

v = Visio('../../../../supervisio/visio', index, '../../../../supervisio/', None, True)
print('Visio started')

while 1:
	start = time.time()
	tris = v.update()
	print("Duration : ", time.time() - start)
	for tri in tris:
		print(tri)
	print()
	time.sleep(1)
