import socket
import time
import binascii
import pycom
import struct
from network import LoRa
from CayenneLPP import CayenneLPP

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

import config

#app_eui = config.app_eui
#app_key = config.app_key

py = Pysense()
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

# Disable heartbeat LED
pycom.heartbeat(False)
print('Led disable at startup')

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an ABP authentication params
#dev_addr = struct.unpack(">l", binascii.unhexlify('0ab8142f'))[0]
#nwk_swkey = binascii.unhexlify('00112c72b32e0a1c5da9bf6a5f2eae3f')
#app_swkey = binascii.unhexlify('c05b8f1a03130f7bebd588586110362e')
dev_addr = config.dev_addr
nwk_swkey =  config.nwk_swkey
app_swkey = config.app_swkey 

# join a network using ABP activation
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey), timeout=0) 

# wait until the module has joined the network
while not lora.has_joined():
    pycom.rgbled(0x140000)
    time.sleep(2.5)
    pycom.rgbled(0x000000)
    time.sleep(1.0)
    print('Not yet joined...')

print('LoraWan ABP joined...')
pycom.rgbled(0x001400)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

while True:
    s.setblocking(True)
    pycom.rgbled(0x000014)
    lpp = CayenneLPP()

    #print('\n\n** 3-Axis Accelerometer (LIS2HH12)')
    #print('Acceleration', li.acceleration())
    #print('Roll', li.roll())
    #print('Pitch', li.pitch())
    #lpp.add_accelerometer(1, li.acceleration()[0], li.acceleration()[1], li.acceleration()[2])
    #lpp.add_gryrometer(1, li.roll(), li.pitch(), 0)

    print('\n\n** Digital Ambient Light Sensor (LTR-329ALS-01)')
    print('Light', lt.light())
    lpp.add_luminosity(1, lt.light()[0])
    lpp.add_luminosity(2, lt.light()[1])

    print('** Humidity and Temperature Sensor (SI7006A20)')
    print('Humidity', si.humidity())
    print('Temperature', si.temperature())
    lpp.add_relative_humidity(1, si.humidity())
    lpp.add_temperature(1, si.temperature())

    mpPress = MPL3115A2(py,mode=PRESSURE)
    print('** Barometric Pressure Sensor with Altimeter (MPL3115A2)')
    print('Pressure (hPa)', mpPress.pressure()/100)
    lpp.add_barometric_pressure(1, mpPress.pressure()/100)

    mpAlt = MPL3115A2(py,mode=ALTITUDE)
    print('Altitude', mpAlt.altitude())
    print('Temperature', mpAlt.temperature())
    lpp.add_gps(1, 0, 0, mpAlt.altitude())
    lpp.add_temperature(2, mpAlt.temperature())

    print('\nSending data (uplink)...')
    s.send(bytes(lpp.get_buffer()))
    s.setblocking(False)
    data = s.recv(64)
    print('Received data (downlink)', data)
    pycom.rgbled(0x001400)
    time.sleep(40)
