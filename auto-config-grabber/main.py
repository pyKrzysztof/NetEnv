import os
import sys
import datetime
import subprocess

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netautomation import SSHDevice
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE


# CISCO_FILES_PATH = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), 'files'), 'cisco'))
# MT_FILES_PATH = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), 'files'), 'mikrotik'))
failures = {}


class WrongFilesystemError(Exception):
    pass


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


def create_dir(address, device_type):
    if device_type == 'cisco':
        origin_path = CISCO_FILES_PATH
    elif device_type == 'mikrotik':
        origin_path = MT_FILES_PATH
    else:
        raise WrongFilesystemError
    directory = address.replace('.', '-', -1)
    path = os.path.join(origin_path, directory)
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.datetime.now()
    date_str = f'{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}-{date.second}'
    path = os.path.join(path, date_str)
    os.makedirs(path)
    return path

def get_config_cisco(*ssh, path):
    address, port, un, pd = ssh
    device = SSHDevice(address, port)
    device.set_credentials(un, pd)
    is_connected = device.connect()
    if is_connected == AUTH_ERROR:
        failures[address] = 'authentication error'
        return 0
    if is_connected == GENERAL_FAILURE:
        failures[address] = 'general failure'
        return 0
    config = device.send_command('more flash:config.text')
    device.client.close()
    with open(os.path.join(path, 'config.text'), 'w') as f:
        f.write(config)

def get_vlan_cisco(*ssh, sftp, path):
    address, port, un, pd = ssh
    device = SSHDevice(address, port)
    device.set_credentials(un, pd)
    is_connected = device.connect()
    if is_connected == AUTH_ERROR:
        failures[address] = 'authentication error'
        return 0
    if is_connected == GENERAL_FAILURE:
        failures[address] = 'general failure'
        return 0
    # ip ssh source-interface <int name> <int num>
    # must be configured, ask if this is the case.
    out = device.send_command(f'copy flash:vlan.dat sftp://{sftp[1]}:{sftp[2]}@{sftp[0]}/{path}')
    print('DEBUG:', out)

def get_mikrotik_backup(*ssh, path):
    command = f'{ssh[2]}:{ssh[3]}@{ssh[0]} -p {ssh[1]} file print'.split()
    print(command)
    # stdin, stdout, stderr = subprocess.run(command.split())
    # print(stdin, stdout, stderr)

def get_data(*args, device_type=''):
    address, port, un, pd, sftp = args
    path = create_dir(address, device_type)
    if device_type == 'cisco':
        get_config_cisco(address, port, un, pd, path)
        get_vlan_cisco(address, port, un, pd, sftp, path)
    elif device_type == 'mikrotik':
        get_mikrotik_backup(address, port, un, pd, path)
    return 1

def cisco_main(sftp):
    pool = open_list('cisco_list.txt')
    for entry in pool:
        params = entry.split()
        try:
            result = get_data(*params, sftp, device_type='cisco')
        except Exception as e:
            failures[params[0]] = e

def mt_main(sftp):
    pool = open_list('mt_list.txt')
    for entry in pool:
        params = entry.split()
        try:
            result = get_data(*params, sftp, device_type='mikrotik')
        except Exception as e:
            failures[params[0]] = e

def main(*sftp):
    # cisco_main(sftp)
    mt_main(sftp)



if __name__ == '__main__':
    with open('sftp-info', 'r') as f:
        addr, un, pd, path = f.read().split()
    cisco_filepath = os.path.join(os.path.join(path, 'files'), 'cisco')
    mt_filepath = os.path.join(os.path.join(path, 'files'), 'mikrotik')
    get_mikrotik_backup('192.168.120.120', 16, 'admin', 'class', sftp=(addr, un, pd), path=mt_filepath)
    sys.exit()
    main(addr, un, pd, cisco_filepath, mt_filepath)

# sshpass -f <(printf '%s\n' 'test') sftp -P 22 admin@192.168.88.1:MikroTik-11011970-1525.backup