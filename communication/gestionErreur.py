
import time

class MyError(Exception):
	def __init__(self, raison):#On entre toutes les erreurs dans un fichier
		file = open('logError', 'a')
		file.write(time.asctime(time.localtime()) + ': ' + raison + '\n')
		file.close()
		print("bjr")