import sys

from context import *

from netautomation import SerialDevice
from netautomation import Handler

PORT = 'COM5'
BAUDRATE = 9600


def main():
    device = SerialDevice(PORT, BAUDRATE)
    handler = Handler()
    handler.bind_device(device)

    device.set_credentials('cisco', 'class')

    connected = device.connect()

    if not connected:
        print('Port is closed. Exiting.')
        sys.exit()
    print('Connection successful.')

    ints = handler.execute('show ip int')
    print(ints)

    handler.execute('exit')

if __name__ == '__main__':
    main()