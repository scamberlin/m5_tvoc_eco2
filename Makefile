.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To erase flash type make erase"
	@echo "To flash firmware type make flash"
	@echo "To push code type make all"
	@echo "To moniror device type make console"
	@echo "To join type make run"
	@echo "------------------------------------"

PORT = /dev/ttyUSB0
SPEED = 115200
CHIPSET = esp32
FIRMWARE = ../firmware/esp32-idf4-20200902-v1.13.bin
BIN = ${HOME}/python/venv/bin/
ESPTOOL = esptool.py
AMPY = ampy
RSHELL = rshell

flash:
	$(BIN)$(ESPTOOL) --chip $(CHIPSET) --port $(PORT) --baud 750000 write_flash -z 0x1000 $(FIRMWARE)

boot: boot.py
	$(BIN)$(AMPY) -p $(PORT) put $<

main: main.py
	$(BIN)$(AMPY) -p $(PORT) put $<

config: config.py
	$(BIN)$(AMPY) -p $(PORT) put $<

adafruit_sgp30: adafruit_sgp30.py
	$(BIN)$(AMPY) -p $(PORT) put $<

bme280: bme280.py
	$(BIN)$(AMPY) -p $(PORT) put $<

all: config adafruit_sgp30 main boot

rshell:
	$(BIN)$(RSHELL) --buffer-size=30 -p $(PORT)

console:
	pyserial-miniterm $(PORT) $(SPEED)

erase:
	$(ESPTOOL) --chip $(CHIPSET) --port $(PORT) erase_flash

run: all console
