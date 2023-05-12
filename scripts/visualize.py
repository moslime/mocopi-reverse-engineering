#!/usr/bin/python3
from bluepy import btle
from scipy.interpolate import interp1d
import socket
import time

# Change this to the MAC address of your tracker
tracker_addr = '3C:38:F4:AE:B6:3D'

# UDP address and port of visualization script
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Whether or not quaternions should be printed
debug = False

cmd_uuid = '0000ff00-0000-1000-8000-00805f9b34fb'
m = interp1d([-8192,8192],[-1,1])
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def hexToQuat(bytes):
    return -m(int.from_bytes(bytes, byteorder='little', signed=True))

class NotificationHandler(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
     try:
       quant_W = hexToQuat(data[8:10])
       quant_A = hexToQuat(data[10:12])
       quant_B = hexToQuat(data[12:14])
       quant_C = hexToQuat(data[14:16])
       msg = "w" + str(quant_W) + "wa" + str(quant_A) + "ab" + str(quant_B) + "bc" + str(quant_C) + "c"
       sock.sendto(bytes(msg, "utf-8"), (UDP_IP, UDP_PORT))
       
       if debug:
         print("==============================")
         print("Raw Hex       : " + ''.join('{:02X}'.format(a) for a in data))
         print("Unknown 0     : " + str(int(data[0])))
         print("Packet Counter: " + str(int.from_bytes(data[1:8], "little")))
         print()
         print("Quat W   : " + str(quant_W))
         print("Quat A   : " + str(quant_A))
         print("Quat B   : " + str(quant_B))
         print("Quat C   : " + str(quant_C))
         #print("UDP Msg  : " + str(msg))
         print()
         print("Unknown 16-17 : " + str(hexToQuat(data[16:18])))
         print("Unknown 18-19 : " + str(hexToQuat(data[18:20])))
         print("==============================")
         print("")

     except:
        print("Exception")

# Connect to device and set BLE notification handler
p = btle.Peripheral(tracker_addr)
p.setDelegate(NotificationHandler())

# Get Service
cmd = p.getServiceByUUID(cmd_uuid)
cmd_ch = cmd.getCharacteristics()[1]

# Send Command(s)
cmd_ch.write(bytearray([0x7e, 0x03, 0x18, 0xd6, 0x01, 0x00, 0x00]), True) #Start Stream

while True:
    if p.waitForNotifications(1.0):
        continue

    print("Waiting...")
