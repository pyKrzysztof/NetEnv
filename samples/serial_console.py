import sys

from context import *

from rev2 import SerialDevice
from rev2 import SerialCommandHandler

if __name__ == '__main__':
    device = SerialDevice(port='/dev/ttyS3')
    device.set_credentials('cisco', 'class')

    handler = SerialCommandHandler('commands.json')
    handler.bind_device(device)

    connected = device.establish_connection()
    if not connected:
        sys.exit()

    while True:
        stdin = input(device.get_prompt() + ' ')
        commands = handler.translate(stdin)
        stdout = handler.execute_commands(commands)
        if not stdout:
            continue
        for out in stdout:
            print(out)