from __future__ import print_function
import serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


# def print_port_info(port: ListPortInfo) -> None:
#     [print('{}: {}'.format(key, value)) for key, value in port.__dict__.items()]
#     print()

# ports = scan_ports('USB-SERIAL CH340')

# [print_port_info(port) for port in scan_ports()]

baud_rate = 115200

def select_port() -> ListPortInfo:
    ports = list_ports.comports()
    port_list = [port for port in ports]
    print('available ports:')
    
    for id, port in enumerate(port_list):
        print('{}: {}'.format(id, port.name))
        print('\tdevice: {}'.format(port.device))
        print('\tdescription: {}'.format(port.description))
        print('\thwid: {}'.format(port.hwid))
        print()
    
    while True:
        selection = int(input('select a port: '))
        if selection not in range(0, len(port_list)):
            print('invalid selection!')
        else:
            return port_list[selection]



with serial.Serial(select_port().device, baud_rate, timeout=1) as ser:
    while True:
        line = ser.readline()
        print(bytes.decode(line), end='')
'''



'''