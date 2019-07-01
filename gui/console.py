import sys

from context import *

from netautomation import SSHDevice
from netautomation import NetEnv

app = NetEnv()

if __name__ == '__main__':
    argv = sys.argv
    host = argv[1]
    un = argv[2]
    pd = argv[3]

    device = SSHDevice(host, visible_console=True)
    device.set_credentials(un, pd)
    try:
        device.establish_connection(show_console=True, do_check_connection=False)
        device.show_console()
        app.MainLoop()
        while True:
            device.update()
    except:
        device.close_connection()
        raise