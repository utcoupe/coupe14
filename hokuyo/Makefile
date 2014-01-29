DEBUG=yes
SDL=no

CC=gcc
SRC_FILES=main.c fast_math.c hokuyoUrg.c lidar.c robot.c protocole_serial.c serial_switch.c serial_defines.c serial_decoder.c serial_types.c compat.c
SRC_DIR=src/
EXEC=hokuyo

LFLAGS=-Wall `urg_c-config --libs` -lm -pthread
CFLAGS=-Wall `urg_c-config --cflags` -std=c99

ifeq ($(DEBUG),yes)
	CFLAGS += -D DEBUG -g
else
	CFLAGS += -Werror
	LFLAGS += -Werror
endif

ifeq ($(SDL),yes)
	SRC_FILES+= gui.c
	LFLAGS+= `sdl-config --libs` 
	CFLAGS+= -D SDL `sdl-config --cflags` 
	EXEC=hokuyo_sdl
endif

SOURCES=$(SRC_FILES:%=$(SRC_DIR)%)
OBJS=$(SOURCES:src/%.c=build/%.o)

all: $(EXEC)

$(EXEC): $(OBJS) 
	$(CC) -o $@ $^ $(LFLAGS)

build/%.o: src/%.c build
	$(CC) -o $@ $(CFLAGS) -c $<

build:
	mkdir build

fast_math.o: fast_math.h
hokuyoUrg.o: hokuyoUrg.h
lidar.o: lidar.h hokuyoUrg.h fast_math.h
main.o: lidar.h gui.h
gui.o: gui.h
robot.o: robot.h 
namedpipe.o: namedpipe.h

clean:
	rm -rf build
mrproper: clean
	rm $(EXEC)

.PHONY: clean
