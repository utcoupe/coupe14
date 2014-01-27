import os
from threading import Thread

FILENAME = "/tmp/lidarPipe"
LIDARPROGRAM = "../hokuyo/hokuyo_sdl"
LIDARARGS = " red pipe"

class Lidar:
    def __init__(self, debug=True):
        self._debug = debug
        self.thread = Thread(target = self.startLidarC)

        try:
            os.remove(FILENAME)
        except OSError:
            pass
        os.mkfifo(FILENAME)

        print("Opening fifo")
        pipe = os.open(FILENAME, os.O_RDONLY|os.O_NONBLOCK)
        self._reader = os.fdopen(pipe) 

        print("lauching c program, waiting for it to open fifo...")
        self.thread.start()

        firstread = self._reader.readline()
        while firstread == "" :
            firstread = self._reader.readline()


        if firstread == "Hi!\n" :
            print("FIFO connected !")
        else :
            raise("FIFO error")

    def startLidarC(self) :
        os.system("pwd")
        os.system(LIDARPROGRAM+LIDARARGS)
        print(LIDARPROGRAM+LIDARARGS+" closed!!!")

    def poll(self):
        r = self._reader.readline()
        if r == "":
            return None
        return list(map(    lambda e: list(map( lambda f:int(f), e.split(":") )), \
                            r[:-1].split(";")[1:] \
                        ))


