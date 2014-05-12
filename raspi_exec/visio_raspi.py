# -*- coding: utf-8 -*-
import os
import sys
import time

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR, "../ia/"))

import event.goals.visio as visio


class Tourelle:
	def __init__(self):
		self.isATourelle = True

	def getPosition(self):
		return (0, 0)

	def getPositionAndAngle(self):
		return (0, 0, 0)


def compute(v_centre, v_coin):
	triangles = v_centre.update()
	triangles += v_centre.update()
	return triangles


def send(triangles, pipe):
	for tri in triangles:
		pipe.write(str(tri.coord[0]) + " " + str(tri.coord[1]) + " " + str(tri.angle)
					+ " " + str(tri.size) + " " + str(tri.color) + " " 
					+ str(tri.isDown) + "\n")
	pipe.write('END\n')
	pipe.flush()


if __name__ == '__main__':
	try:
		path = sys.argv[1]
		color = sys.argv[2]
	except:
		print('[CAM ]  Not enough arguments : visio_raspi path_pipe color')
		sys.exit()

	path_to_exec = path + "/supervisio/visio"
	path_pipe = path + "/config/raspi/pipe_cameras"
	config_path = path + "/config/visio/visio_tourelle_" + color + "/"
	success = False
	index = 0

	while index < 3 and not success:
		print("[CAM ]  Executing visio with config at", config_path, "on port video" + str(index))
		try:
			tourelle = Tourelle()
			v_centre = visio.Visio(path_to_exec, index, config_path, tourelle, True)
			v_coin = visio.Visio(path_to_exec, index+1, config_path, tourelle, True)
			success = True
		except BaseException as e:
			print("[CAM ]  Failed to open visio programs : "+str(e))
			index += 1

	if not success:
		sys.exit()

	print("[CAM ]  Attempting to open fifo at",path_pipe)
	try:
		pipe = open(path_pipe, "w")
	except BaseException as e:
		print("[CAM ]  Failed to open pipe : "+str(e))
		sys.exit()
	print("[CAM ]  Fifo opened")

	conti = True
	while(conti):
		start = time.time()
		triangles = []
		try:
			triangles = compute(v_centre, v_coin)
			send(triangles, pipe)
			#print("Detected", len(triangles), "in", (time.time() - start), "seconds")
		except BaseException as e:
			conti = False
			print("Failed to compute and send triangles :", str(e))

			triangles = []

	print('Closing')
	v.close()
	sys.exit()
