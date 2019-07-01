from context import *

from netautomation import SSHDevice
from netautomation import NetEnv

app = NetEnv()

device = SSHDevice('127.0.0.1', visible_console=True)
device.establish_connection(do_check_connection=False)

app.MainLoop()