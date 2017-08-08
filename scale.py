import serial
import serial.tools.list_ports
import platform
import time
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
    ser = serial.Serial(port, baudrate=9600)#, timeout=.5)
    ser.flushInput()
    ser.flushOutput()
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


def write_to_file(data, time, filename='result.txt'):
    with open(filename,'a') as f:
        f.write(str("%.2f" %time) + '\t' + str(data) + '\n')


def write_header_in_file(filename):
    with open(filename, 'a') as f:
        f.write('\nTIME(s)\tWEIGHT(g)\n')
        f.close()

scalePort = get_scale_address()
the_time = 0
filename = 'result.txt'

write_header_in_file(filename)
print 'TIME(s)\tWEIGHT (g)'

while 1:
    start = time.time()
    reading = read_serial(scalePort)
    stop = time.time()
    the_time += (stop - start)
    write_to_file(reading, the_time, filename)

    print "%.2f"%the_time ,'\t', reading

