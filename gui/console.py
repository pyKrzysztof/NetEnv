import sys

from context import *

from netautomation import SSHDevice
from netautomation import NetEnv

app = NetEnv()

if __name__ == '__main__':
    argv = sys.argv
    host = argv[1]

    device = SSHDevice(host, visible_console=True)
    # device.establish_connection(show_console=True)
    device.show_console()

    app.MainLoop()
