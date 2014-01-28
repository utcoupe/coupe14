VISUAL=no
DEBUG=yes
EXEC=visio

SRCS_FILES=main.c compat.c serial_switch.c serial_types.c serial_decoder.c serial_defines.c protocole.c traitement.c

CC=gcc
CFLAGS+=-Wall `pkg-config --cflags opencv`
LDFLAGS+=-Wall `pkg-config --libs opencv`
BUILD_DIR=build/
SRC_DIR=src/

OBJS=$(SRCS_FILES:%.c=$(BUILD_DIR)%.o)
SRCS=$(SRCS_FILES:%=$(SRC_DIR)%)

ifeq ($(VISUAL),yes)
	CFLAGS += -D VISUAL
endif

ifeq ($(DEBUG),yes)
	CFLAGS += -D DEBUG
else
	CFLAGS += -Werror
	LFLAGS += -Werror
endif

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $^ $(LDFLAGS) -o $@

$(BUILD_DIR)%.o: $(SRC_DIR)%.c build
	$(CC) $< $(CFLAGS) -c -o $@

visio.o: global.h traitement.h
traitement.o: traitement.h

clean:
	rm -rf build/
mrproper: clean
	rm -f $(EXEC)

build/:
	mkdir build

.PHONY: clean mrproper
