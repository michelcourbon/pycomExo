from network import WLAN
import machine
import ubinascii
import config

print(ubinascii.hexlify(machine.unique_id(),':').decode())
print(ubinascii.hexlify(WLAN().mac().sta_mac,':').decode())

print("wait scanning wireless network..")
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
     print('Network found with ssid= '+net.ssid)     
print('scanning SSID finished !!')

if wlan.isconnected():
     print(wlan.ifconfig())
else:
     for net in nets:
          if (net.ssid == config.WIFI_SSID):
               print("try to connect.. with security : ",net.sec)
               wlan.connect(net.ssid, auth=(net.sec,config.WIFI_PASS), timeout=3000)
               while not wlan.isconnected():
                    machine.idle() # save power while waiting
               print(wlan.ifconfig())
               print("Connected with IP address:" + wlan.ifconfig()[0])
