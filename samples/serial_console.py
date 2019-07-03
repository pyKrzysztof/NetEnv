import sys

from context import *
from rev2 import SerialDevice


device = SerialDevice('COM5')
device.set_credentials('cisco', 'class')
connected = device.connect()

if not connected:
    print('Port is closed. Exiting.')
    sys.exit()
print('Connection successful.')

print(device.send_command('show version'))
