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


handler = Handler()
handler.bind_device(device)
ints = handler.execute('show ip int')
print(ints)


handler.execute('exit')