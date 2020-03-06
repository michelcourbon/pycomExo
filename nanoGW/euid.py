from network import LoRa
import binascii
import machine

WIFI_MAC = binascii.hexlify(machine.unique_id()).upper()
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]
print ("======== euid ===========")
print("  Wifi gatewayId = ", GATEWAY_ID)
print("  lorawan Mac Address = ", binascii.hexlify(LoRa(mode=LoRa.LORAWAN).mac()) )
