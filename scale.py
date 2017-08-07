import serial
import serial.tools.list_ports
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import platform
import re


def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports


def get_scale_address_OSX(portsList):
    # Check ports for a Duplex Serial USB connection
    for i in range(0, len(portsList)):
        # Need the two steps, first get the full address then split
        comPort = portsList[i]
        comPort = str(comPort).split(' ')

        if comPort[-3] + comPort[-2] + comPort[-1] == 'USB<->Serial':
            return comPort[0]   # Returns first part of address list
        else:
            pass
    # If Weight not found throw error
    raise TypeError('Could not find weight adress')


def choose_scale_address():
    ports = get_ports()
    for i in range(0,len(ports)):
        print ports[i]

    port = raw_input(">>> Choose serial port address: ")
    return port


def get_scale_address(portsList = []):
    # If portsList is empty, get ports
    if not portsList:
        portsList = get_ports()
    else:
        pass

    # Check OS
    os = platform.system()
    if os == 'Darwin':
        comPort = get_scale_address_OSX(portsList)
        return comPort
    else:
        pass


def read_serial(port, raw_output = False):
    ser = serial.Serial(port, baudrate=9600, timeout=5)
    reading = str(ser.readline())

    if raw_output is False:
        p = re.search("([+-]) *([0-9]*\.[0-9]*)", reading)
        result = ''
        if p is not None:
            result = p.group(1) + p.group(2)
            return float(result)
        return float('nan')
    else:
        return reading


weightPort = get_scale_address() # OR choose_scale_address()
reading = 0

while 1:
    reading = read_serial(weightPort)
    print reading, type(reading)




