from getpass import getpass
import sys

from context import *
from netautomation import SSHDevice
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE


HOST = '192.168.0.12'

def main():
    device = SSHDevice(HOST)

    un = input('Username: ')
    pd = getpass('Password: ')
    device.set_credentials(un, pd)
    del un
    del pd
    
    connected = device.connect()

    if connected == AUTH_ERROR:
        print('Authentication Error.')
        sys.exit()
    elif connected == GENERAL_FAILURE:
        print('General Failure.')
        sys.exit()

    try:
        while True:
            stdin = input('> ').strip()
            if stdin == '!exit':
                break
            out = device.send_command(stdin)
            print(out)
    except Exception as e:
        print(e)
        pass
    device.close()


if __name__ == '__main__':
    main()