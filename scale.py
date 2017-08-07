import serial
import serial.tools.list_ports
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import platform
import re


def get_ports():
    return serial.tools.list_ports.comports()


def get_scale_address_unix(ports):
    # Check ports for a Duplex Serial USB connection
    for port in ports:
        properties = str(port).split(' - ')
        name = properties[0]
        identifier = properties[-1]
        if identifier == 'USB <-> Serial':
            return name
    else:
        raise IOError('Could not find scale address')


def choose_scale_address():
    for port in get_ports():
        print port

    scale_port = raw_input(">>> Choose serial port address: ")
    return scale_port


def get_scale_address(ports=get_ports()):
    # Check OS
    os = platform.system()
    if os in ('Darwin', 'Linux'):
        port = get_scale_address_unix(ports)
    elif os in ('Windows'):
        raise NotImplementedError('Windows not implemented... yet!')
    else:
        raise NotImplementedError('Unknown platform %s' % os)
    return port


def read_serial(port, raw_output=False):
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


scalePort = get_scale_address() # OR choose_scale_address()
while 1:
    reading = read_serial(scalePort)
    print reading, type(reading)
