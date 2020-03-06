#!/usr/bin/env python
import binascii
import struct

# OTAA.. activation
#app_eui = binascii.unhexlify('4060b33ef9ead0d9c5360b2f791f3cd0')
#app_key = binascii.unhexlify('3c13f429303bf2293efe2cb5423c10e8') 

# ABP... activation
# copy and paste from Chirpstack AS
address ='0b 27 5f ed'
nwSession = 'ed 4e ab 89 27 59 8a 97 0b f4 45 8b 7b 46 41 e0'
appSession = 'bb 2d cf f5 9b ca 47 d3 aa a0 34 a6 8f 60 98 7a'

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify(address.replace(" ","")))[0]
nwk_swkey = binascii.unhexlify(nwSession.replace(" ",""))
app_swkey = binascii.unhexlify(appSession.replace(" ",""))
