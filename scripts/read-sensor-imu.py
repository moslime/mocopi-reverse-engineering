#!/usr/bin/python3
from bluepy import btle
from scipy.interpolate import interp1d
import time
import struct
import requests
import numpy as np
import traceback

# If you'd like to compare the numbers to the IMU in your phone, download phyphox https://phyphox.org/, start the acceleration (without g) experiment, 
# allow remote access (3 dots > allow remote access), replace PP_ADDRESS with the IP of your phone and change phyphox to true.

tracker_addr = '3C:38:F4:AE:B6:3D' # Tracker address
PP_ADDRESS = "http://192.168.1.111:8080" # Phyphox device IP address
formatted = True # Changing this to false will show each byte sperately as integers
phyphox = False # True will print data from phyphox (only enable if you already have it set up!)

# shouldnt need to mess with
cmd_uuid = '0000ff00-0000-1000-8000-00805f9b34fb'
quatRange = interp1d([-8192,8192],[-1,1])

def hexToQuat(bytes):
    return -quatRange(int.from_bytes(bytes, byteorder='little', signed=True))
def hexToFloat(bytes):
    dt = np.dtype(np.float16)
    dt = dt.newbyteorder('<')
    return np.frombuffer(bytes, dtype=dt)
def hexToInt(bytes):
    return int.from_bytes(bytes, byteorder='little', signed=True)
def furthest_from_0(a):
    return max(a, key=lambda x: abs(x[0]))
def is_equal(a,b):
    return a==b
def get_phone_accel():
    PP_CHANNELS = ["accX","accY","accZ"]
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    x = data["buffer"]["accX"]["buffer"]
    y = data["buffer"]["accY"]["buffer"]
    z = data["buffer"]["accZ"]["buffer"]
    return x, y, z

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
     try:
       if formatted:
        #print("Unknown 0     : " + str(int(data[0])))
        #print("Counter 1-7   : " + str(int.from_bytes(data[1:8], "little")))
        #print()
        #print("Quat W  8-9   : " + str(hexToQuat(data[8:10])))
        #print("Quat X  10-11 : " + str(hexToQuat(data[10:12])))
        #print("Quat Y  12-13 : " + str(hexToQuat(data[12:14])))
        #print("Quat Z  14-15 : " + str(hexToQuat(data[14:16])))	
        #print()
        #print("From last packet:")
        #print("Quat W  16-17 : " + str(hexToQuat(data[16:18])))
        #print("Quat X  18-19 : " + str(hexToQuat(data[18:20])))
        #print("Quat Y  20-21 : " + str(hexToQuat(data[20:22])))
        #print("Quat Z  22-23 : " + str(hexToQuat(data[22:24])))
        #print()
        
        rotation_quaternion = np.array([hexToQuat(data[16:18]), hexToQuat(data[18:20]), hexToQuat(data[20:22]), hexToQuat(data[22:24])])
        acceleration_vector = np.array([hexToFloat(data[28:30])[0], hexToFloat(data[26:28])[0], hexToFloat(data[24:26])[0]])
        rotation_quaternion /= np.linalg.norm(rotation_quaternion)
        acceleration_quaternion = np.concatenate(([0], acceleration_vector))
        rotated_quaternion = rotation_quaternion * acceleration_quaternion * np.conjugate(rotation_quaternion)
        rotated_acceleration = np.array(rotated_quaternion[1:])
        #print("Rotated Acceleration:", rotated_acceleration)
        
        far = furthest_from_0([hexToFloat(data[24:26]), hexToFloat(data[26:28]), hexToFloat(data[28:30])])
        far3 = 0

        if phyphox:
           phone = get_phone_accel()
           far2 = furthest_from_0([phone[0], phone[1], phone[2]])
        #far3 = furthest_from_0([hexToFloat(data[30:32]), hexToFloat(data[32:34]), hexToFloat(data[34:36])])
        print("==============================" +
        #"\nRaw Hex       : " + ''.join('{:02X}'.format(a) for a in data) +
        ("\n+  " if is_equal(far, hexToFloat(data[24:26])) else "\n-  ") + "24 - 25 : " + str(hexToFloat(data[24:26])) +
        ("\n+  " if is_equal(far, hexToFloat(data[26:28])) else "\n-  ") + "26 - 27 : " + str(hexToFloat(data[26:28])) + 
        ("\n+  " if is_equal(far, hexToFloat(data[28:30])) else "\n-  ") + "28 - 29 : " + str(hexToFloat(data[28:30])) +
        ("\nRotated (ignore for now):") +
        ("\n+  " if is_equal(far3, rotated_acceleration[0]) else "\n-  ") + "24 - 25 : " + str(rotated_acceleration[0]) +
        ("\n+  " if is_equal(far3, rotated_acceleration[1]) else "\n-  ") + "26 - 27 : " + str(rotated_acceleration[1]) + 
        ("\n+  " if is_equal(far3, rotated_acceleration[2]) else "\n-  ") + "28 - 29 : " + str(rotated_acceleration[2])
        )
        if phyphox:
          print(
          ("\n+  " if is_equal(far2, phone[0]) else "\n-  ") + "Phone X : " + str(phone[0]) + 
          ("\n+  " if is_equal(far2, phone[1]) else "\n-  ") + "Phone Y : " + str(phone[1]) + 
          ("\n+  " if is_equal(far2, phone[2]) else "\n-  ") + "Phone Z : " + str(phone[2])
          )
        
        #("\n+  " if is_equal(far3, hexToFloat(data[30:32])) else "\n-  ") + "30 - 31 : " + str(hexToFloat(data[30:32])) + 
        #("\n+  " if is_equal(far3, hexToFloat(data[32:34])) else "\n-  ") + "32 - 33 : " + str(hexToFloat(data[32:34])) + 
        #("\n+  " if is_equal(far3, hexToFloat(data[34:36])) else "\n-  ") + "34 - 35 : " + str(hexToFloat(data[34:36]))
        
        #print("26 - 27 : " + 	str(hexToFloat(data[26:28])))
        #print("28 - 29 : " + str(hexToFloat(data[28:30])))
        #print("30 - 31 : " + str(hexToFloat(data[30:32])))
        #print("32 - 33 : " + str(hexToFloat(data[32:34])))
        #print("34 - 35 : " + str(hexToFloat(data[34:36])))
        #print("24 : " + str(int(data[24])))
        #print("25 : " + str(int(data[25])))
        #print("26 : " + str(int(data[26])))
        #print("27 : " + str(int(data[27])))
        #print("28 : " + str(int(data[28])))
        #print("29 : " + str(int(data[29])))
        #print("30 : " + str(int(data[30])))
        #print("31 : " + str(int(data[31])))
        #print("32 : " + str(int(data[32])))
        #print("33 : " + str(int(data[33])))
        #print("34 : " + str(int(data[34])))
        #print("35 : " + str(int(data[35])))

       else:
        for i in data:
         print(i)

     except Exception as e:
        print("Exception:" + str(e))
        traceback.print_exc()
     print("==============================")
     print("")

p = btle.Peripheral(tracker_addr)
p.setDelegate( MyDelegate() )
p.setMTU(40)
#Get Service
cmd = p.getServiceByUUID(cmd_uuid)
cmd_ch = cmd.getCharacteristics()[1]

#Send Commands
cmd_ch.write(bytearray([0x7e, 0x03, 0x18, 0xd6, 0x01, 0x00, 0x00]), True) #Start Stream

while True:
    if p.waitForNotifications(1.0):
        continue

    print("Waiting...")
