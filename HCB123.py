import serial
import serial.tools.list_ports as sertools
import time
import re
import platform


class HCB123:
    def __init__(self):
        self.port = None
        self.SERIAL = False
        self.initialize_scale()
        self.raw_data = 'nan'
        self.data = 'nan'
        self.timer = 0
        self.file_index = 0
        self.filename = 'Result' + str(self.file_index) + ".txt"
        print("\n>>> Serial Connection established: %s" % self.port.device)

    def get_ports(self):
        return sertools.comports()

    def set_filename(self, filename):
        if not str(filename).endswith(".txt"):
            self.filename = str(filename) + ".txt"
        else:
            self.filename = str(filename)

    def initialize_scale(self):
        ports = self.get_ports()
        for port in ports:
            if "FTDI" in str(port.manufacturer):
                self.port = port
                self.SERIAL = self.open_port(port)
        if not self.SERIAL:
            print("\n\nERROR: Did not find any connected ADAM HCB123 devices")
            print("       these ports were found:\n")
            print("%3s %35s -  %20s  %30s  " % ("NUM", "ADDRESS", "MANUFACTURER", "DESCRIPTION"))
            for n, port in enumerate(ports):
                print("%3g %35s -   %20s  %30s  " % (n, port.device, port.manufacturer, port.description))
            num = input("\nPick the desired port number: ")
            chosenport = ports[num]
            print("You picked: %s" % chosenport.device)
            self.port = port
            self.SERIAL = self.open_port(port)

    def open_port(self, port, baud=9600):
        return serial.Serial(port.device, baud)

    def restart_port(self):
        self.SERIAL.close()
        time.sleep(1)
        self.open_port(self.port)

    def close_port(self):
        return serial.Serial.close(self.SERIAL)

    def read_serial(self, raw_data=False):
        self.SERIAL.close()
        # time.sleep(1)
        self.open_port(self.port)
        self.SERIAL = self.open_port(self.port)
        self.SERIAL.flush()
        self.raw_data = self.SERIAL.readline()

        if raw_data is False:  # Return parsed data as float
            parsed_data = re.search(b"([+-]) *([0-9]*\.[0-9]*)", self.raw_data)
            if parsed_data is not None:
                self.data = str(parsed_data.group(1)).strip('\'b') + str(parsed_data.group(2)).strip(
                    '\'b')  # str(parsed_data.group(1)) + str(parsed_data.group(2))
                return float(self.data)
            return float("nan")
        else:  # Return raw data from serial
            return self.raw_data

    def write_to_file(self):
        self.get_data()
        with open(self.filename, 'a') as f:
            f.write(str("%.2f" % self.timer) + '\t' + str(self.data) + '\n')

    def write_header_in_file(self):
        with open(self.filename, 'a') as f:
            f.write('\nTIME(s)\tWEIGHT(g)\n')
            f.close()

    def get_data(self):
        start = time.time()
        self.read_serial()
        stop = time.time()
        self.timer += (stop - start)
        return self.timer, self.data

    def print_data(self):
        self.get_data()
        print(str("%.2f" % self.timer) + "\t" + str(self.data))  # , type(self.data))

    def print_header(self):
        print('\nTIME(s)\tWEIGHT(g)\n')

    def print_startup_message(self):
        print("\n**********************")
        print("    ADAM HCB123 ")
        print("**********************")
        print("Choose command number:")
        print("1 - Show scale reading")
        print("2 - Print to file")
        print("----------------------")


if __name__ == '__main__':
    system_os = platform.system()
    print (system_os)
    scale = HCB123()
    scale.restart_port()
    scale.print_startup_message()

    try:
        for retry in range(3):
            command = str(input(">>> "))
            if command == '1':
                scale.print_header()
                while True:
                    scale.print_data()

            elif command == '2':
                if system_os == 'Darwin': #(OSX)
                    user_filename = raw_input('>>> Choose filename:\n>>> ')
                else:
                    user_filename = input('>>> Choose filename: \n>>> ')
                scale.set_filename(user_filename)
                scale.write_header_in_file()
                print("----------------------")
                print("\nPrinting to file: " + scale.filename)
                while True:
                    scale.write_to_file()
                    print(str("%.2f" % scale.timer) + "\t" + str(scale.data))
            else:
                print(">>> Sorry, " + "\"" + str(command) + "\"" + " is not a valid command. Try again")
        print("ERROR: You have tried too many times.")
    except KeyboardInterrupt:
        scale.close_port()
        if command == '2':
            print(">>> Aborted by user. Data saved to " + scale.filename)
        else:
            print(">>> Aborted by user. No data saved")
