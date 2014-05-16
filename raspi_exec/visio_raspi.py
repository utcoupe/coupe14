# -*- coding: utf-8 -*-
import os
import sys
import time
import signal

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR, "../ia/"))

import event.goals.visio as visio

PATH_CONFIG = "/config/visio/visio_tourelle_"
PATH_TO_EXEC = "/supervisio/visio"
PATH_PIPE = "/config/raspi/pipe_cameras"
DIST_SAME_TRI = 100


class Tourelle(dict):
	def __init__(self):
		self.isATourelle = True
		self["getPosition"] = (0, 0)
		self["getPositionAndAngle"] = (0, 0, 0)

	def getPosition(self):
		return (0, 0)

	def getPositionAndAngle(self):
		return (0, 0, 0)


def compute(v_centre, v_coin):
	triangles = v_centre.update()
	triangles_coin = v_centre.update()
	for tri in triangles_coin:
		for t in triangles:
			if tri.dist2(t) < DIST_SAME_TRI:
				triangles.append(tri)
				break

	return triangles


def send(triangles, pipe):
	for tri in triangles:
		if tri.color == 'RED':
			int_color = 0
		elif tri.color == 'YELLOW':
			int_color = 1
		elif tri.color == 'BLACK':
			int_color = 2
		else:
			int_color = -1
		pipe.write(str(tri.coord[0]) + " " + str(tri.coord[1]) + " " + str(tri.angle) \
					+ " " + str(tri.size) + " " + str(int_color) + " " + str(int(tri.isDown)) + "\n")
	pipe.write('END\n')
	pipe.flush()


def close():
	os.kill(os.getppid(), signal.SIGUSR1)
	sys.exit()

if __name__ == '__main__':
	index = 0
	print("[CAM ]  Starting cam client")
	try:
		path = sys.argv[1]
		color = sys.argv[2]
		try:
			index = sys.argv[3]
		except:
			pass
	except:
		print('[CAM ]  Not enough arguments : visio_raspi path_pipe color')
		close()

	path_to_exec = path + PATH_TO_EXEC
	path_pipe = path + PATH_PIPE
	config_path = path + PATH_CONFIG
	if color == 'red':
		config_path += 'red/'
	elif color == 'yellow':
		config_path += 'yellow/'
	else:
		print("[CAM ]  Unknown color :", color)
		close()
	success = False

	#clean des fichiers chiants
	print('[CAM ]  Removing old videos')
	os.system("rm " + path + "/config/raspi/pipe_*")
	os.system("rm " + path + "/config/visio/visio_tourelle_red/video* " \
					+ path + "/config/visio/visio_tourelle_yellow/video*")

	print("[CAM ]  Executing visio with config at", config_path, "on port video" + str(index))
	try:
		tourelle = Tourelle()
		v_centre = visio.Visio(path_to_exec, index, config_path, tourelle, True)
		v_coin = visio.Visio(path_to_exec, index+1, config_path, tourelle, True)
		print('[CAM ]  Successfully opened visio on ports', index, 'and', index+1)
		success = True
	except BaseException as e:
		print("[CAM ]  Failed to open visio programs : "+str(e))
		if v_centre is not None:
			v_centre.close()
		if v_coin is not None:
			v_coin.close()

	if not success:
		close()

	print("[CAM ]  Attempting to open fifo at",path_pipe)
	try:
		pipe = open(path_pipe, "w")
	except BaseException as e:
		print("[CAM ]  Failed to open pipe : "+str(e))
		close()
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
	v_coin.close()
	v_centre.close()
	close()
