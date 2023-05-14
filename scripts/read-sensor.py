#!/usr/bin/python3
from bluepy import btle
from scipy.interpolate import interp1d
import time

# Change this to the MAC address of your tracker
tracker_addr = '3C:38:F4:AE:B6:3D'
cmd_uuid = '0000ff00-0000-1000-8000-00805f9b34fb'

# Changing this to false will show each byte sperately as integers
formatted = True	

m = interp1d([-8192,8192],[-1,1])

def hexToQuat(bytes):
    return -m(int.from_bytes(bytes, byteorder='little', signed=True))
    
class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
     try:
       print("==============================")
       print("Raw Hex       : " + ''.join('{:02X}'.format(a) for a in data))
       if formatted:
        print("Unknown 0     : " + str(int(data[0])))
        print("Counter 1-7   : " + str(int.from_bytes(data[1:8], "little")))
        print()
        print("Quat W  8-9   : " + str(hexToQuat(data[8:10])))
        print("Quat X  10-11 : " + str(hexToQuat(data[10:12])))
        print("Quat Y  12-13 : " + str(hexToQuat(data[12:14])))
        print("Quat Z  14-15 : " + str(hexToQuat(data[14:16])))	
        print()
        print("From last packet:")
        print("Quat W  16-17 : " + str(hexToQuat(data[16:18])))
        print("Quat X  18-19 : " + str(hexToQuat(data[18:20])))
        print("Quat Y  20-21 : " + str(hexToQuat(data[20:22])))
        print("Quat Z  22-23 : " + str(hexToQuat(data[22:24])))
        print()
        print("Unknown:")        
        print("24 : " + str(int(data[24])))
        print("25 : " + str(int(data[25])))
        print("26 : " + str(int(data[26])))
        print("27 : " + str(int(data[27])))
        print("28 : " + str(int(data[28])))
        print("29 : " + str(int(data[29])))
        print("30 : " + str(int(data[30])))
        print("31 : " + str(int(data[31])))
        print("32 : " + str(int(data[32])))
        print("33 : " + str(int(data[33])))
        print("34 : " + str(int(data[34])))
        print("35 : " + str(int(data[35])))

       else:
        for i in data:
         print(i)

     except:
        print("Exception")
     print("==============================")
     print("")
p = btle.Peripheral(tracker_addr)
p.setDelegate( MyDelegate() )
p.setMTU(50)
#Get Service
cmd = p.getServiceByUUID(cmd_uuid)
cmd_ch = cmd.getCharacteristics()[1]

#Send Commands
cmd_ch.write(bytearray([0x7e, 0x03, 0x18, 0xd6, 0x01, 0x00, 0x00]), True) #Start Stream

while True:
    if p.waitForNotifications(1.0):
        continue

    print("Waiting...")
