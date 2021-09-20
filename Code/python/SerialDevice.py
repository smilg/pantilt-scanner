import serial
import serial.tools.list_ports as list_ports
from serial.tools.list_ports_common import ListPortInfo


class SerialDevice:
    STANDARD_BAUDS = (50, 75, 110, 134, 150, 200, 300, 600,
                        1200, 1800, 2400, 4800, 9600, 19200,
                        38400, 57600, 115200)

    EXTENDED_BAUDS = (230400, 460800, 500000, 576000, 921600,
                        1000000, 1152000, 1500000, 2000000,
                        2500000, 3000000, 3500000, 4000000)

    ARDUINO_HIDS = ((0x2341, 0x0043), (0x2341, 0x0001),
                    (0x2A03, 0x0043), (0x2341, 0x0243),
                    (0x0403, 0x6001), (0x1A86, 0x7523))

    def __init__(self, port = None, baud = 115200, log_name = 'log.txt') -> None:
        self.ser = serial.Serial(timeout = 1)
        self.connected = False
        self.port = port
        self.baud = self.confirm_baud(baud)
        self.ser.baudrate = self.baud
        self.log_file = open(log_name, 'a+')

        # try to autoselect a port if no port was specified
        if not port:
            arduino_ports = self.autodetect_ports()
            for port in arduino_ports:
                if not self.connected:
                    print('possible arduino port detected:')
                    print_port_info(port)
                    self.connect(port)
            if not self.connected:
                print('no recognized ports found. manually select one:')
                
                self.connect(self.manual_select_port())
        else:
            self.connect(port)
    
    def __del__(self) -> None:
        self.ser.close()
        self.log_file.close()

    def autodetect_ports(self) -> list:
        ports = list_ports.comports()
        arduino_ports = []
        for port in ports:
            if (port.vid, port.pid) in SerialDevice.ARDUINO_HIDS:
                arduino_ports.append(port)
        return arduino_ports

    def manual_select_port(self) -> ListPortInfo:
        ports = list_ports.comports()
        port_list = [port for port in ports]
        print('found ports:')
        for id, port in enumerate(port_list):
            print('{}:'.format(id))
            print_port_info(port)
            print()

        while True:
            selection = input('select a port: ').strip()
            if selection.isnumeric():
                selection = int(selection)
            if selection not in range(0, len(port_list)):
                print('invalid selection!')
            else:
                return port_list[int(selection)]

    def connect(self, port: ListPortInfo) -> None:
        if yesno_confirm('connect with baud rate {}?'.format(self.baud)):
            self.port = port
            try:
                self.ser.port = self.port.device
                self.ser.baudrate = self.baud
                self.ser.open()
                self.connected = True
                print('opened port {}'.format(port.name))
            except:
                print('can\'t connect to port {}! is the port already in use?'.format(self.port.device))
                pass
        else:
            print('not connecting to port {}.'.format(port.name))

    def confirm_baud(self, baud: int) -> int:
        print('the currently selected baud rate is {}.'.format(baud))
        
        if yesno_confirm('would you like to change it?'):
            baud_choice = ''
            confirmed = False
            while True:
                baud_choice = input('enter a new baud rate: ').strip()
                if not baud_choice.isnumeric():
                    print('invalid input! please enter a number.')
                else:
                    baud_choice = int(baud_choice)
                    if baud_choice in SerialDevice.EXTENDED_BAUDS:
                        print('baud rate {} is not standard, but may still be supported on some machines.'.format(baud_choice))
                        if yesno_confirm('are you sure you want to select baud rate {}?'.format(baud_choice)):
                            print('using baud rate {}.'.format(baud_choice))
                            return int(baud_choice)
                    elif baud_choice in SerialDevice.STANDARD_BAUDS:
                        print('using baud rate {}.'.format(baud_choice))
                        return int(baud_choice)
                    else:
                        print('baud rate {} is not standard, and is likely not supported.'.format(baud_choice))
                        if yesno_confirm('are you sure you want to select baud rate {}?'.format(baud_choice)):
                            print('using baud rate {}.'.format(baud_choice))
                            return int(baud_choice)
        else:
            return baud

    def read(self) -> str:
        line = self.ser.readline().decode()
        if len(line) > 0:
            self.log_file.write(line.rstrip()+'\n')
        return line

    def write(self, string) -> None:
        self.ser.write('{}\r'.format(string).encode())


def print_port_info(port: ListPortInfo) -> None:
    print('\tname: {}'.format(port.name))
    print('\tdevice: {}'.format(port.device))
    print('\tdescription: {}'.format(port.description))
    print('\thwid: {}'.format(port.hwid))


def yesno_confirm(message) -> bool:
    confirm_choice = ''
    while confirm_choice not in ('y', 'n'):
        confirm_choice = input("{} (y/n) ".format(message)).lower().strip()
        if confirm_choice not in ('y', 'n'):
            print('please enter "y" or "n"')
    return confirm_choice == 'y'


if __name__ == '__main__':
    dev = SerialDevice()
    while True:
        line = dev.read()
        if len(line) > 0:
            print(line, end='')