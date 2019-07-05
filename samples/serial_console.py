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

    try:
        while True:
            stdin = input('>').strip()
            if stdin == '!exit':
                handler.execute('exit')
                break
            stdout = handler.execute(stdin)
            print(stdout)
    except:
        handler.execute('exit')
        raise

if __name__ == '__main__':
    main()