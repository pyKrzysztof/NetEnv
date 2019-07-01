import sys
import os

from context import *

from rev2 import SSHDevice
from rev2 import SSHCommandHandler


if __name__ == '__main__':
    device = SSHDevice(host='192.168.10.254')
    device.set_device_type('cisco_ios')
    device.set_credentials('cisco', 'class')
    
    handler = SSHCommandHandler('commands.json')
    handler.bind_device(device)

    device.establish_connection()
    try:
        while True:
            stdin = input(device.get_prompt() + ' ')
            commands = handler.translate(stdin)
            stdout = handler.execute_commands(commands)
            if not stdout:
                continue
            for out in stdout:
                print(out)
    except:
        device.close_connection()
        raise