import os
import sys
import datetime

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netautomation import SSHDevice
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE


failures = {}


def open_list(filename):
    pool = []
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)), 'r') as f:
        for line in f:
            pool.append(line)
    return pool

def write_failures():
    with open('failures.txt', 'w') as f:
        for key, value in failures.items():
            f.write(f'{key} -> {value}\n')

def write_files(config, vlans, address):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))
    directory = address.replace('.', '-', -1)
    path = os.path.join(path, directory)
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.datetime.now()
    date_str = f'{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}-{date.second}'
    path = os.path.join(path, date_str)
    os.makedirs(path)
    with open(os.path.join(path, 'config.text'), 'w') as f:
        f.write(config)
    with open(os.path.join(path, 'vlan.dat'), 'w') as f:
        f.write(vlans)

def get_config(device):
    config = device.send_command('more flash:config.text')
    device.client.close()
    return config

def get_vlan(address, port, un, pd):
    return 'not implemented yet'

def get_data(*args):
    address, port, un, pd = args
    port = int(port)
    device = SSHDevice(address, port)
    device.set_credentials(un, pd)
    is_connected = device.connect()
    if is_connected == AUTH_ERROR:
        failures[address] = 'authentication error'
        return 0
    if is_connected == GENERAL_FAILURE:
        failures[address] = 'general failure'
        return 0
    config = get_config(device)
    vlans = get_vlan(address, port, un, pd)
    return config, vlans


def main(filename):
    pool = open_list(filename)
    for entry in pool:
        params = entry.split()
        try:
            result = get_data(*params)
            if not result:
                continue
            write_files(*result, params[0])
        except Exception as e:
            failures[params[0]] = e
        


if __name__ == '__main__':
    main(sys.argv[1])