from lidar import Lidar
import time

lidar = Lidar();


while True:
	p = lidar.poll()
	if(p != None):
		print(p)
	time.sleep(0.050)


