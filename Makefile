MAC_PORT = "/dev/tty.SLAB_USBtoUART"
LNX_PORT = "/dev/ttyACM0"
PORT = $(LNX_PORT)


usage:
	@echo "* shell"
	@echo "* upload-as-main FILE=<file>"
	@echo "* upload-file FILE=<file>"
	@echo "* install-gol"
	@echo "* install-info-panel"
	# @echo "* secrets"

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

install-info-panel: /media/$(USER)/CIRCUITPY/settings.toml
	# --- Main
	cp info_panel/main.py /media/$(USER)/CIRCUITPY/main.py
	# --- Libs
	cp lib/aio.py /media/$(USER)/CIRCUITPY/lib
	cp lib/dates.py /media/$(USER)/CIRCUITPY/lib
	cp lib/chronos.py /media/$(USER)/CIRCUITPY/lib
	cp lib/led_matrix.py /media/$(USER)/CIRCUITPY/lib
	cp lib/my_wifi.py /media/$(USER)/CIRCUITPY/lib
	cp -a lib/colors /media/$(USER)/CIRCUITPY/lib
	# --- Package
	cp -a info_panel /media/$(USER)/CIRCUITPY/

secrets: lib/secrets.py

lib/secrets.py: .secrets
	./bin/gen_secrets.py
	cp lib/secrets.py /media/$(USER)/CIRCUITPY/

.PHONY: shell upload-as-main upload-file install-gol install-info-panel secrets
