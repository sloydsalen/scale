import serial
import serial.tools.list_ports
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import os
import platform
import re


def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports


def get_weight_adress_OSX(portsList):
    # Check ports for a Duplex Serial USB connection
    for i in range(0, len(portsList)):
        # Need the two steps, first get the full adress then split
        comPort = portsList[i]
        comPort = str(comPort).split(' ')

        if comPort[-3] + comPort[-2] + comPort[-1] == 'USB<->Serial':
            return comPort[0]   # Returns first part of adress list
        else:
            pass
    # If Weight not found throw error
    raise TypeError('Could not find weight adress')
    #print 'Could not find weight adress'


def get_weight_adress(portsList = []):
    # If portsList is empty, get ports
    if not portsList:
        portsList = get_ports()
        # print 'Got Ports my self'
    else:
        pass

    # Check OS
    os = platform.system()
    if os == 'Darwin':
        comPort = get_weight_adress_OSX(portsList)
        return comPort
    else:
        pass


def read_serial(port):
    ser = serial.Serial(port, baudrate=9600, timeout=5)
    ser.flush()
    #reading = ser.readline().strip("+      ").strip(" g \r\n").strip('-      ')#.decode('ascii')
    reading = str(ser.readline())
    #print reading
    p = re.search("([+-]) *([0-9]*\.[0-9]*)", reading)
    result = ''
    if p is not None:
        result = p.group(1) + p.group(2)
    #reading = ser.readline()#.strip(" g \r\n")

    return float(result)


def plot_serial_data(data):
    #ser = serial.Serial(port,baudrate=9600,timeout=1)

    plt.ion()  # set plot to animated

    ydata = [0] * 50
    ax1 = plt.axes()

    # make plot
    line, = plt.plot(ydata)
    plt.ylim([10, 40])

    # start data collection
    while True:
        #data = ser.readline().rstrip()  # read data from serial
        # port and strip line endings
        if len(data.split(".")) == 2:
            ymin = float(min(ydata)) - 10
            ymax = float(max(ydata)) + 10
            plt.ylim([ymin, ymax])
            ydata.append(data)
            del ydata[0]
            line.set_xdata(np.arange(len(ydata)))
            line.set_ydata(ydata)  # update the data
            plt.draw()  # update the plot


weightPort = get_weight_adress()
reading = 0
while 1:
    reading = read_serial(weightPort)
    print reading , type(reading)

'''
ports = subprocess.check_output(['bash','-c', "ls /dev/cu.*"])
print "*** USB ports ***"
print ports.split("\n")[:-1]


port = raw_input(">>> Choose usb port: ")


i = 0
data = []

while (i < 10):
    ser = serial.Serial(port, baudrate=9600, timeout=5)
    ser.flush()
    weight = ser.readline().strip("+      ").strip(" g \r\n")
    #weight = ser.readline().decode('ascii')
    data.append(weight)
    print weight
    i = i+1

print "length: " + str(len(data))
print data


onlyData = [float(x) for x in data[1:]]

print onlyData
print onlyData[0] + onlyData[1]

'''
