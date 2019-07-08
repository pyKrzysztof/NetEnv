import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netautomation import SSHDevice
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE

failures = {}
pool = []

def get_data(*args):
    address, port, un, pd = args
    port = int(port)
    device = SSHDevice(address, port)
    device.set_credentials(un, pd)
    is_connected = device.connect()
    if is_connected == AUTH_ERROR:
        failures[address] = 'authentication error'
    if is_connected == GENERAL_FAILURE:
        failures[address] = 'general failure'

def write_failures():
    with open('failures.txt', 'w') as f:
        for key, value in failures.items():
            f.write(f'{key} -> {value}\n')

def open_list(file):
    

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'list.txt')), 'r') as f:
    for line in f:
        pool.append(line)

for entry in pool:
    get_data(entry)
    
