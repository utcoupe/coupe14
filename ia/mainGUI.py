from time import sleep
from gui.gui import GUI
from lidar.lidar import Lidar




gui = GUI()
lidar = Lidar()

while True :
	print(".", end="")
	robots = lidar.poll()
	if(robots != None):
		gui.displayRobots(robots)
	sleep(0.1)
