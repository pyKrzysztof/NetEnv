import os
import sys
import datetime
import subprocess
import datetime
import socket
import time

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netautomation import SSHDevice
from netautomation import AUTH_ERROR
from netautomation import GENERAL_FAILURE


class SSHConnectionException(Exception):
    pass

PATH = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), 'files'), 'cisco'))
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'tftp_path')), 'r') as f:
    TFTP_PATH = f.read()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

IP = get_ip()


def create_files(address):
    if not os.path.exists(PATH):
        os.makedirs(PATH)
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

def get_vlans(*args, path):
    device = SSHDevice(args[0], args[1])
    device.set_credentials(args[2], args[3])
    device.connect(single_attempt=True)
    # out = device.send_command(f'copy flash:vlan.dat tftp://{IP}/vlan.dat')
    print('connected')
    shell = device.client.invoke_shell()

    # turn off paging
    shell.send('terminal length 0\n')
    time.sleep(1)
    resp = shell.recv(9999)
    output = resp.decode('ascii').split(',')

    shell.send(f'copy flash:vlan.dat tftp://{IP}/vlan.dat')
    shell.send('\n')
    time.sleep(1)
    resp = shell.recv(9999)
    output = resp.decode('ascii').split(',')
    print (''.join(output))

    for _ in range(4):
        shell.send('\n')
        time.sleep(1)
        resp = shell.recv(9999)
        output = resp.decode('ascii').split(',')
        print(''.join(output))
    os.system(f'bash move.sh {os.path.join(TFTP_PATH, "vlan.dat")} {os.path.join(path, "vlan.dat")}')
    # os.system(f'bash move.sh config.text {os.path.join(path, "config.text")}')
    return 1

def get_config(*args, path):
    device = SSHDevice(args[0], args[1])
    device.set_credentials(args[2], args[3])
    connected = device.connect()
    if not connected:
        raise SSHConnectionException
    # out = device.send_command(f'copy flash:config.text tftp://{IP}/config.text')
    print('connected')
    shell = device.client.invoke_shell()

    # turn off paging
    shell.send('terminal length 0\n')
    time.sleep(1)
    resp = shell.recv(9999)
    output = resp.decode('ascii').split(',')

    shell.send(f'copy flash:config.text tftp://{IP}/startup-config')
    shell.send('\n')
    time.sleep(1)
    resp = shell.recv(9999)
    output = resp.decode('ascii').split(',')
    print (''.join(output))

    for _ in range(4):
        shell.send('\n')
        time.sleep(1)
        resp = shell.recv(9999)
        output = resp.decode('ascii').split(',')
        print(''.join(output))

    os.system(f'bash move.sh {os.path.join(TFTP_PATH, "config.text")} {os.path.join(path, "config.text")}')
    # os.system(f'bash move.sh config.text {os.path.join(path, "config.text")}')
    return 1

def get_backup_files(*args):
    path = create_files(args[0])
    get_vlans(*args, path=path)
    get_config(*args, path=path)

def main():
    failures = {}
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cisco_list.txt'), 'r') as f:
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
    # print(IP)