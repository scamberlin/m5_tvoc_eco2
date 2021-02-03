import config
import network
import time
import utime
import machine
import neopixel
import adafruit_sgp30

from time import sleep
from machine import I2C

try:
  np = neopixel.NeoPixel(machine.Pin(27), 1) # valid for Atom lite (m5stack)
  np[0] = (0, 0, 64)  # set to blue
  np.write()
except Exception as e:
  print("Exception: {}".format(e))

def fade(ppm):
  for i in range(0, 4 * 256, 8):
    if (i // 256) % 2 == 0:
      val = i & 0xff
    else:
      val = 255 - (i & 0xff)
    if ppm >= 1200:
      np[0] = (val, 0, 0) # fade to red
    elif ppm < 1200 and ppm >= 850:
      np[0] = (val, val, 0) # fade to orange
    elif ppm < 850:
      np[0] = (0, val, 0) # fade to green
    else:
      np[0] = (0, 0, val) # fade to blue
    try:
      np.write()
    except Exception as e:
      print("Exception: {}".format(e))
    time.sleep_ms(60)

i2c = I2C(sda=machine.Pin(26), scl=machine.Pin(32), freq=100000) # valid for Atom lite (m5stack)

# scanning for I2C devices
devices = i2c.scan()
if len(devices) == 0:
  print("Error: no I2C device !")
else:
  for d in devices:
    print("Decimal address: ",d," | Hexa address: ",hex(d))


# initialize SGP30 sensor
try:
  sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c,address=0x58)
  print("SGP30 serial #", [hex(i) for i in sgp30.serial])
  sgp30.iaq_init()
  print("Waiting 5 seconds for SGP30 initialization.")
  time.sleep(5)
except Exception as e:
  print("Exception: {}".format(e))

# main
while True:
  try:
    co2_eq, tvoc = sgp30.iaq_measure()
    print('co2eq = ' + str(co2_eq) + ' ppm \t tvoc = ' + str(tvoc) + ' ppb')
    fade(co2_eq)
  except Exception as e:
    print("Exception: {}".format(e))
