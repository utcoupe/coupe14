from visio import Visio

v = Visio('../../supervisio/build/bin/visio', 1)

while 1:
	print(v.update())
