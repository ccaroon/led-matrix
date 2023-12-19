MAC_PORT = "/dev/tty.SLAB_USBtoUART"
LNX_PORT = "/dev/ttyACM0"
PORT = $(LNX_PORT)


usage:
	@echo "* shell"
	@echo "* upload-as-main FILE=<file>"
	@echo "* upload-file FILE=<file>"
	@echo "* install-gol"
	@echo "* info-panel"

shell:
	picocom $(PORT) -b115200

upload-as-main:
ifneq ($(FILE),)
	cp $(FILE) /media/$(USER)/CIRCUITPY/main.py
else
	echo "ERROR: Must Specify a filename with FILE=filename"
endif

upload-file:
ifneq ($(FILE),)
	cp $(FILE) /media/$(USER)/CIRCUITPY/
else
	echo "ERROR: Must Specify a filename with FILE=filename"
endif

/media/$(USER)/CIRCUITPY/settings.toml: settings.toml
	cp settings.toml /media/$(USER)/CIRCUITPY/

install-playground:
	cp playground/main.py /media/$(USER)/CIRCUITPY/main.py
	cp lib/led_matrix.py /media/$(USER)/CIRCUITPY/lib
	cp -a playground /media/$(USER)/CIRCUITPY/

install-gol: /media/$(USER)/CIRCUITPY/settings.toml
	cp game_of_life/main.py /media/$(USER)/CIRCUITPY/main.py
	cp lib/led_matrix.py /media/$(USER)/CIRCUITPY/lib
	cp -a game_of_life /media/$(USER)/CIRCUITPY/

# Lib
LIB_SRC_FILES = $(shell find lib -name "*.py")
LIB_DEST_FILES = $(LIB_SRC_FILES:%=/media/$(USER)/CIRCUITPY/%)
libs: $(LIB_DEST_FILES)

# InfoPanel
## TODO: what about data files?
IP_SRC_FILES = $(shell find info_panel -name "*.py")
IP_DEST_FILES = $(IP_SRC_FILES:%=/media/$(USER)/CIRCUITPY/%)
## InfoPanel -- Main
/media/$(USER)/CIRCUITPY/info_panel/main.py: info_panel/main.py
	cp $< $@
	cp $< /media/$(USER)/CIRCUITPY/main.py
## InfoPanel -- Package
info-panel: libs $(IP_DEST_FILES) /media/$(USER)/CIRCUITPY/settings.toml


/media/$(USER)/CIRCUITPY/%.py: %.py
	cp $< $@


.PHONY: shell upload-as-main upload-file install-gol info-panel
