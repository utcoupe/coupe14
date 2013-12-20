VISUAL=yes
DEBUG=yes
EXEC=test

SRCS_FILES=main.c traitement.c

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

$(EXEC): $(OBJS)
	$(CC) $^ $(LDFLAGS) -o $@

$(BUILD_DIR)%.o: $(SRC_DIR)%.c build
	$(CC) $< $(CFLAGS) -c -o $@

main.o: global.h traitement.h
traitement.o: traitement.h

clean:
	rm -rf build/
mrproper: clean
	rm -f $(EXEC)

main.o: global.h

build/:
	mkdir build

.PHONY: clean mrproper
