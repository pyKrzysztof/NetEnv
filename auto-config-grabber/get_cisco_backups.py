import os
import sys
import datetime
import subprocess
import datetime

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netautomation import SSHDevice
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE


class SSHConnectionException(Exception):
    pass

PATH = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), 'files'), 'cisco'))

def create_files(address):
    device_folder_name = address.replace('.', '-', -1)
    path = os.path.join(PATH, device_folder_name)
    if not os.path.exists(path):
        os.makedirs(path)

    now = datetime.datetime.now()
    backup_folder_name = f'{now.day}_{now.month}_{now.year}-{now.hour}_{now.minute}_{now.second}'
    backup_folder_path = os.path.join(path, backup_folder_name)
    try:    os.makedirs(backup_folder_path)
    except:    pass
    return backup_folder_path

def get_backup_files(*args):
    get_vlans(*args)
    get_config(*args)

def main():
    failures = {}
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mt_list.txt'), 'r') as f:
        data = f.readlines()
        try:
            devices = [entry.split() for entry in data]
        except IndexError:
            devices = [devices]
            devices = [entry.split() for entry in data]
        for device in devices:
            device[1] = int(device[1])
    for device in devices:
        try:
            get_backup_files(*device)
        except Exception as e:
            raise
            failures[device[0]] = e
    with open('failures.txt', 'w') as f:
        for key, value in failures.items():
            f.write(f'{key}: {value}')

if __name__ == '__main__':
    main()