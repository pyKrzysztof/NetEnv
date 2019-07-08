import sys
import time
import os

path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'))
sys.path.insert(0, path)

from netautomation import SSHDevice
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE


def get_vlans(address, un, pd):
    device = SSHDevice(address)
    device.set_credentials(un, pd)
    connected = device.connect()

    if connected == AUTH_ERROR:    return 0
    elif connected == GENERAL_FAILURE:    return 0

    vlan_data = device.send_command('more flash:vlan.dat')
    device.client.close()
    with open('vlan.dat', 'w') as f:
        f.write(vlan_data)
    return 1

def get_config(address, un, pd):
    device = SSHDevice(address)
    device.set_credentials(un, pd)
    connected = device.connect()

    if connected == AUTH_ERROR:    return 0
    elif connected == GENERAL_FAILURE:    return 0

    config = device.send_command('more flash:config.text')
    device.client.close()
    with open('config.text', 'w') as f:
        f.write(config)
    return 1

if __name__ == '__main__':
    address = input('Address: ').strip()
    un = input('Username: ').strip()
    pd = input('Password: ').strip()
    result = get_config()
    if result:
        print('config.text read')
    result = get_vlans()
    if result:
        print('vlan.dat read')
