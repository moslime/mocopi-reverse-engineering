#!/usr/bin/python3
from bluepy import btle
from scipy.interpolate import interp1d
import socket
import time
import struct

# consts
tracker_addr = '3C:38:F4:AE:B6:3D'
UDP_IP = "127.0.0.1" # SlimeVR Server
UDP_PORT = 6969 # SlimeVR Server
UDP_IP2 = "127.0.0.1" # pyteapot.py
UDP_PORT2 = 5005 # pyteapot.py
debug = True
cmd_uuid = '0000ff00-0000-1000-8000-00805f9b34fb'
m = interp1d([-8192,8192],[-1,1])
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

test_handshake = {
    'packet_type': 3,
    'packet_id': 0,
    'board': 0,
    'imu': 0,
    'mcu' : 0,
    'build' : 8,
    'firm': "OwOTrack8",
    'mac' : "111111"
}

example_imu = {
    'packet_type': 17,
    'packet_id': 1,
    'sensor_id': 0,
    'data_type': 1,
    'quat': {
        'x': 0,
        'y': 0,
        'z': 0,
        'w': 0
    },
    'calibration_info': 0
}

def build_imu_packet(mapping):
    buffer = b''
    buffer += struct.pack('>L', mapping['packet_type'])  # unsigned 32 bit integer
    buffer += struct.pack('>Q', mapping['packet_id'])  # unsigned 64 bit integer
    buffer += struct.pack('B', mapping['sensor_id'])  # 8 bit integer
    buffer += struct.pack('B', mapping['data_type'])  # 8 bit integer
    buffer += struct.pack('>ffff', *mapping['quat'].values())  # four 32 bit floats
    buffer += struct.pack('B', mapping['calibration_info'])  # 8 bit integer
    return buffer
    
def build_handshake(mapping):
    buffer = b''
    buffer += struct.pack('>L', mapping['packet_type'])  # unsigned 32 bit integer
    buffer += struct.pack('>Q', mapping['packet_id'])  # unsigned 64 bit integer
    buffer += struct.pack('24x')
    buffer += struct.pack('B', mapping['board'])
    buffer += struct.pack('B', mapping['imu'])
    buffer += struct.pack('B', mapping['mcu'])
    buffer += struct.pack('B', mapping['build'])
    buffer += struct.pack('B', len(mapping['firm']))
    buffer += struct.pack(str(len(mapping['firm'])) + 's', mapping['firm'].encode('UTF-8'))
    buffer += struct.pack('6s', mapping['mac'].encode('UTF-8'))
    buffer += struct.pack('B', 255)
    return buffer

def hexToQuat(bytes):
    return m(int.from_bytes(bytes, byteorder='little', signed=True))

class NotificationHandler(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
     try:
       quant_W = hexToQuat(data[8:10])
       quant_A = hexToQuat(data[10:12])
       quant_B = hexToQuat(data[12:14])
       quant_C = hexToQuat(data[14:16])	
       
       # build packet
       example_imu['quat']['x'] = -quant_A
       example_imu['quat']['y'] = -quant_B
       example_imu['quat']['z'] = quant_C
       example_imu['quat']['w'] = quant_W
       example_imu['packet_id'] +=1 
       imu = build_imu_packet(example_imu)
       sock.sendto(imu, (UDP_IP, UDP_PORT))
       msg = "w" + str(quant_W) + "wa" + str(quant_A) + "ab" + str(quant_B) + "bc" + str(quant_C) + "c"
       sock.sendto(bytes(msg, "utf-8"), (UDP_IP2, UDP_PORT2))
       
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

# bluetooth stuff
p = btle.Peripheral(tracker_addr)
p.setDelegate(NotificationHandler())
cmd = p.getServiceByUUID(cmd_uuid)
cmd_ch = cmd.getCharacteristics()[1]

# send handshake
handshake = build_handshake(test_handshake)
sock.sendto(handshake, (UDP_IP, UDP_PORT))
print("Handshake")
time.sleep(.1)

# Send Command(s)
cmd_ch.write(bytearray([0x7e, 0x03, 0x18, 0xd6, 0x01, 0x00, 0x00]), True) #Start Stream

while True:
     if p.waitForNotifications(1.0):
         continue
     print("Waiting...")
