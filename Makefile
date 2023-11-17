MAC_PORT = "/dev/tty.SLAB_USBtoUART"
LNX_PORT = "/dev/ttyACM0"
PORT = $(LNX_PORT)


usage:
	@echo "* shell"
	@echo "* upload-as-main FILE=<file>"
	@echo "* upload-file FILE=<file>"
	@echo "* install-gol"
	@echo "* secrets"

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

install-playground:
	cp playground/main.py /media/$(USER)/CIRCUITPY/main.py
	cp lib/led_matrix.py /media/$(USER)/CIRCUITPY/lib
	cp -a playground /media/$(USER)/CIRCUITPY/

install-gol:
	cp game_of_life/main.py /media/$(USER)/CIRCUITPY/main.py
	cp lib/led_matrix.py /media/$(USER)/CIRCUITPY/lib
	cp -a game_of_life /media/$(USER)/CIRCUITPY/

secrets: lib/secrets.py

lib/secrets.py: .secrets
	./bin/gen_secrets.py
	cp lib/secrets.py /media/$(USER)/CIRCUITPY/

.PHONY: shell upload-as-main upload-file
