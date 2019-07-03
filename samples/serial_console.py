import sys

from context import *
from rev2 import SerialDevice


class DeviceNotBoundException(Exception):
    pass

class NotImplementedYet(Exception):
    pass

class Handler:
    
    def __init__(self):
        pass

    def bind_device(self, device):
        self.device = device

    def execute(self, command):
        if command.startswith('!'):
            return self.handle_auto_command(command[1:])
        return self.handle_regular_command(command)

    def handle_regular_command(self, command, ):
        if not hasattr(self, 'device'):
            raise DeviceNotBoundException
        out = self.device.send_command(command, new_line=True, do_print=False)
        if 'show' in command:
            for _ in range(10):
                if out.strip().endswith('--More--'):
                    out = out.replace(' --More--', '')
                    temp = self.device.send_command(' ', new_line=False, do_print=False, delay=.1)
                    out += temp
                    # Next result is wrongly formatted (ALWAYS), you can later find '\r\n' in previous line
                    # and from that calculate accurate indices from current space. (This is true for show ip int br)
                temp = self.device.send_command('', new_line=False, do_print=False, delay=.5)
                if temp.strip().endswith('--More--'):
                    temp = temp.replace(' --More--', '')
                    out += temp
                    temp = self.device.send_command(' ', new_line=False, do_print=False, delay=.1)
                    # Next result is wrongly formatted (ALWAYS), you can later find '\r\n' in previous line
                    # and from that calculate accurate indices from current space. (This is true for show ip int br)
                out += temp
        return out

    def handle_auto_command(self, command):
        raise NotImplementedYet


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