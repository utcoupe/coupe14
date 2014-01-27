VISUAL=no
DEBUG=yes
EXEC_VISIO=visio
EXEC_COM=com

SRCS_FILES_VISIO=visio.c traitement.c pipe.c
SRCS_FILES_COM=

CC=gcc
CFLAGS+=-Wall `pkg-config --cflags opencv`
LDFLAGS+=-Wall `pkg-config --libs opencv`
BUILD_DIR=build/
SRC_DIR=src/

OBJS_VISIO=$(SRCS_FILES_VISIO:%.c=$(BUILD_DIR)%.o)
SRCS_VISIO=$(SRCS_FILES_VISIO:%=$(SRC_DIR)%)

OBJS_COM=$(SRCS_FILES_COM:%.c=$(BUILD_DIR)%.o)
SRCS_COM=$(SRCS_FILES_COM:%=$(SRC_DIR)%)

ifeq ($(VISUAL),yes)
	CFLAGS += -D VISUAL
endif

ifeq ($(DEBUG),yes)
	CFLAGS += -D DEBUG
else
	CFLAGS += -Werror
	LFLAGS += -Werror
endif

all: $(EXEC_VISIO) $(EXEC_COM)

$(EXEC_VISIO): $(OBJS_VISIO)
	$(CC) $^ $(LDFLAGS) -o $@

$(EXEC_COM): $(OBJS_COM)
	$(CC) $^ $(LDFLAGS) -o $@
$(BUILD_DIR)%.o: $(SRC_DIR)%.c build
	$(CC) $< $(CFLAGS) -c -o $@

visio.o: global.h traitement.h
traitement.o: traitement.h
pipe.o: pipe.h

clean:
	rm -rf build/
mrproper: clean
	rm -f $(EXEC)

build/:
	mkdir build

.PHONY: clean mrproper
