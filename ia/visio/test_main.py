from visio import Visio
import sys
import time

try:
	index = sys.argv[1]
except:
	index = 0

v = Visio('../../supervisio/build/bin/visio', index)

while 1:
	start = time.time()
	print(v.update())
	print("Duration : ", time.time() - start)
	time.sleep(1)
