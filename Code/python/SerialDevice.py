from helpers import yesno_confirm
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

    def __init__(self, port = None, baud = 115200) -> None:
        self.ser = serial.Serial(timeout = 1)
        self.connected = False
        self.port = port
        self.baud = self.confirm_baud(baud)
        self.ser.baudrate = self.baud

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
        '''
        close the serial connection when the object is deleted
        '''
        self.ser.close()

    def autodetect_ports(self) -> list:
        '''
        check if any of the visible COM ports have matching Arduino
        (or clone) HIDS, and return a list of the ones that do.

        Returns:
            list: a list of ListPortInfo objects that match Arduino HIDS
        '''
        ports = list_ports.comports()
        arduino_ports = []
        for port in ports:
            if (port.vid, port.pid) in SerialDevice.ARDUINO_HIDS:
                arduino_ports.append(port)
        return arduino_ports

    def manual_select_port(self) -> ListPortInfo:
        '''
        have the user manually select a serial port to connect to

        Returns:
            ListPortInfo: the serial port chosen by the user.
        '''
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
        '''
        confirm connection to a serial port, and connect (or don't).

        Args:
            port (ListPortInfo): the port to possibly be connected to.
        '''
        if yesno_confirm('connect with baud rate {}?'.format(self.baud)):
            self.port = port
            try:
                self.ser.port = self.port.device
                self.ser.baudrate = self.baud
                self.ser.open()
                self.connected = True
                print('opened port {}'.format(port.name))
            except:
                print(('can\'t connect to port {}! is '+\
                    'the port already in use?').format(self.port.device))
                pass
        else:
            print('not connecting to port {}.'.format(port.name))

    def confirm_baud(self, baud: int) -> int:
        '''
        ask the user if they want to change the baud rate,
        and change it to what they want.

        Args:
            baud (int): the currently selected baud rate.

        Returns:
            int: the user's choice of baud rate.
        '''
        print('the currently selected baud rate is {}.'.format(baud))
        
        if yesno_confirm('would you like to change it?'):
            baud_choice = ''
            while True:
                baud_choice = input('enter a new baud rate: ').strip()
                if not baud_choice.isnumeric():
                    print('invalid input! please enter a number.')
                else:
                    baud_choice = int(baud_choice)
                    if baud_choice in SerialDevice.EXTENDED_BAUDS:
                        print(('baud rate {} is not standard, but may still '+\
                                'be supported on some machines.').format(baud_choice))
                        if yesno_confirm(('are you sure you want to select '+\
                                'baud rate {}?').format(baud_choice)):
                            print('using baud rate {}.'.format(baud_choice))
                            return int(baud_choice)
                    elif baud_choice in SerialDevice.STANDARD_BAUDS:
                        print('using baud rate {}.'.format(baud_choice))
                        return int(baud_choice)
                    else:
                        print(('baud rate {} is not standard, and is likely '+\
                                'not supported.').format(baud_choice))
                        if yesno_confirm(('are you sure you want to select '+\
                                'baud rate {}?').format(baud_choice)):
                            print('using baud rate {}.'.format(baud_choice))
                            return int(baud_choice)
        else:
            return baud

    def read(self) -> str:
        '''
        read the serial input buffer

        Returns:
            str: the contents of the serial input buffer
        '''
        line = ''
        if self.connected:
            line = self.ser.readline().decode()
        return line

    def write(self, string: str) -> None:
        '''
        send something over the serial port.

        Args:
            string (str): data to send over the serial port.
        '''
        if self.connected:
            self.ser.write('{}\r'.format(string).encode())


def print_port_info(port: ListPortInfo) -> None:
    '''
    list information about a specific serial port.

    Args:
        port (ListPortInfo): the serial port to print info about.
    '''
    print('\tname: {}'.format(port.name))
    print('\tdevice: {}'.format(port.device))
    print('\tdescription: {}'.format(port.description))
    print('\thwid: {}'.format(port.hwid))


if __name__ == '__main__':
    # debug stuff, used to monitor the port when testing
    dev = SerialDevice()
    while True:
        line = dev.read()
        if len(line) > 0:
            print(line, end='')