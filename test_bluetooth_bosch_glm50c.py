#!/usr/bin/env python

"""
Author: Prudhvi raj
"""
import os
import bluetooth
import struct
from requests.exceptions import ConnectionError

class GLM(object):
    socket = None
    bluetooth_address = None
    connected = False

    cmds = {
        'measure':          b'\xC0\x40\x00\xEE',
        'laser_on':         b'\xC0\x41\x00\x96',
        'laser_off':        b'\xC0\x42\x00\x1E',
        'backlight_on':     b'\xC0\x47\x00\x20',
        'backlight_off':    b'\xC0\x48\x00\x62'
    }

    status = {
        0:  'ok',
        1:  'communication timeout',
        3:  'checksum error',
        4:  'unknown command',
        5:  'invalid access level',
        8:  'hardware error',
        10: 'device not ready',
    }

    def __init__(self, *args, **kwargs):
        self.bluetooth_address = kwargs.get("bluetooth_address", None)
        print(self.bluetooth_address)
        if self.bluetooth_address is None:
            self.find()

    def connect(self):
        try:
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            print(self.bluetooth_address, self.port,bluetooth.RFCOMM)
            self.socket.connect((self.bluetooth_address, self.port))
            
            self.connected = True
        except:
            self.socket.close()
            self.connected = False
            raise ConnectionError

    def find(self):
        dev = self.__class__.__name__
        print('Searching for BOSCH ' + dev)
        nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True, flush_cache=True, lookup_class=False)
        print(nearby_devices)
        for index, val in enumerate(nearby_devices):
            addr, name = val
            if dev in name.upper():
                self.bluetooth_address = addr
                print('Found BOSCH ' + dev + ' @', self.bluetooth_address)
                return

    def measure(self):
        self.socket.send(self.cmds['measure'])
        data = self.socket.recv(1024)
        print('received:', data)

        if self.status[data[0]] is 'ok':
            try:
                # distance to object from top of device
                distance = int(struct.unpack("<L", data[2:6])[0])*0.05
                print(distance, 'mm')
                return distance
            except:
                print('corrupt data received, try again')
                return -1
        else:
            return -1

    def measure_from_top(self):
        return self.measure()

    def measure_from_tripod_socket(self):
        m = self.measure()
        if m is -1: return m
        return m+40

    def measure_from_back(self):
        m = self.measure()
        if m is -1: return m
        return m+110

    def turn_laser_on(self):
        self.socket.send(self.cmds['laser_on'])
        self.socket.recv(1024)

    def turn_laser_off(self):
        self.socket.send(self.cmds['laser_off'])
        self.socket.recv(1024)

    def turn_backlight_on(self):
        self.socket.send(self.cmds['backlight_on'])
        self.socket.recv(1024)

    def turn_backlight_off(self):
        self.socket.send(self.cmds['backlight_off'])
        self.socket.recv(1024)

    def raw_command(self, cmd):
        if isinstance(cmd, bytes):
            #print('sending:\t', cmd)
            self.socket.send(cmd)
            data = self.socket.recv(1024)
            #print('received:\t', data)

            status = self.status[data[0]]
            #print(self.status[data[0]])

            return (data, status)
        else:
            print('no bytes, ignoring')
            return None

    def find_bluetooth_services(self):
        services = bluetooth.find_service(address=self.bluetooth_address)
        if len(services) > 0:
            print("found %d services on %s" % (len(services), self.bluetooth_address))
            print(services)
        else:
            print("no services found")

    def close(self):
        self.socket.close()


class GLM50C(GLM):

    def __init__(self, *args, **kwargs):
        self.port = 0x0005
        super().__init__(*args, **kwargs)

class GLM100C(GLM):
    def __init__(self, *args, **kwargs):
        self.port = 0x0001
        super().__init__(*args, **kwargs)


if __name__ == "__main__":

    # Add argparse in a future.
    try:
        device = GLM100C()
    except:
        print('No devices GLM100C found')

    try:
        device = GLM50C()
        print(device)
    except:
        print('No devices GLM50C found')
        os.sys.exit()
   try:
        print("Trying to connect with "+ device.__class__.__name__)
        device.connect()
    except ConnectionError:
        print ('Connection Error. Can\'t connect with ' + device.__class__.__name__)

    if device.connected:
        print('Connected BOSCH '+ device.__class__.__name__ +'  @', device.bluetooth_address)

        try:
            print('\ntype \'m\' to measure, \n\'lon\' or \'loff\' to turn laser on/off, \n\'bon\' or \'boff\' to turn backlight on/off,\n\'x\' to exit\n')

            while True:
                data = input()
                if data == 'm':
                    distance = device.measure()
                    if distance > 0:
                        print(distance, 'mm from top of device')
                        print(distance+40.0, 'mm from tripod socket')
                        print(distance+110.0, 'mm from back of device')
                elif data == 'lon':
                    device.turn_laser_on()
                elif data == 'loff':
                    device.turn_laser_off()
                elif data == 'bon':
                    device.turn_backlight_on()
                elif data == 'boff':
                    device.turn_backlight_off()
                elif data == 'x':
                    device.close()
                    print('Connection to BOSCH ' + device.__class__.__name__ + ' closed')
                    break

        except KeyboardInterrupt:
            device.close()
            print('Connection to '+ device.__class__.__name__+' closed')
    else:
        print('Could not connect to '+ device.__class__.__name__ )
