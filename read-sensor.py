#!/usr/bin/python3
from bluepy import btle
import time

tracker_addr = '3C:38:F4:AE:B6:3D'
cmd_uuid = '0000ff00-0000-1000-8000-00805f9b34fb'


formatted = True

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
     try:
       print("==============================")
       print("Raw Hex       : " + ''.join('{:02X}'.format(a) for a in data))
       if formatted:
        #print("Timestamp: " + str(time.time()))
        print("Unknown 0     : " + str(int(data[0])))
        print("Counter 1-7   : " + str(int.from_bytes(data[1:8], "little")))
        print()
        print("Unknown 8-9   : " + str(int.from_bytes(data[8:10], "little")))
        print("Unknown 10-11 : " + str(int.from_bytes(data[10:12], "little")))
        print("Unknown 12-13 : " + str(int.from_bytes(data[12:14], "little")))
        print("Unknown 14-15 : " + str(int.from_bytes(data[14:16], "little")))
        print("")
        print("Unknown 16-17 : " + str(int.from_bytes(data[16:18], "little")))
        print("Unknown 18-19 : " + str(int.from_bytes(data[18:20], "little")))

       else:
        print("0 : " + str(int(data[0])))
        print("1 : " + str(int(data[1])))
        print("2 : " + str(int(data[2])))
        print("3 : " + str(int(data[3])))
        print("4 : " + str(int(data[4])))
        print("5 : " + str(int(data[5])))
        print("6 : " + str(int(data[6])))
        print("7 : " + str(int(data[7])))
        print("8 : " + str(int(data[8])))
        print("9 : " + str(int(data[9])))
        print("10: " + str(int(data[10])))
        print("11: " + str(int(data[11])))
        print("12: " + str(int(data[12])))
        print("13: " + str(int(data[13])))
        print("14: " + str(int(data[14])))
        print("15: " + str(int(data[15])))
        print("16: " + str(int(data[16])))
        print("17: " + str(int(data[17])))
        print("18: " + str(int(data[18])))
        print("19: " + str(int(data[19])))

     except:
        print("Exception")
     print("==============================")
     print("")
p = btle.Peripheral(tracker_addr)
p.setDelegate( MyDelegate() )

#Start Notifications
cmd = p.getServiceByUUID(cmd_uuid)
cmd_ch = cmd.getCharacteristics()[1]
cmd_ch.write(bytearray([0x7e, 0x03, 0x18, 0xd6, 0x01, 0x00, 0x00]), True)
#Give tracker time to start sending data
time.sleep(3)

while True:
    if p.waitForNotifications(1.0):
        # handleNotification() was called
        continue

    print("Waiting...")
