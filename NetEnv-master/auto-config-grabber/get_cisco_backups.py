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


THIS_PATH = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.abspath("C:/users/dude/Documents/DEV-backup/cisco")

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'tftp_path')), 'r') as f:
    TFTP_PATH = os.path.abspath(f.read())
    
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'tftp_address')), 'r') as f:
    IP = f.read()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


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
    move_file(os.path.join(TFTP_PATH, "vlan.dat"), 
              os.path.join(path, "vlan.dat"))
    return 1

def get_config(*args, path):
    device = SSHDevice(args[0], args[1])
    device.set_credentials(args[2], args[3])
    connected = device.connect()
    if not connected:
        raise SSHConnectionException
    shell = device.client.invoke_shell()

    # turn off paging
    shell.send('terminal length 0\n')
    time.sleep(1)
    resp = shell.recv(9999)
    output = resp.decode('ascii').split(',')

    shell.send(f'copy flash:config.text tftp://{IP}/config.text')
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

    move_file(os.path.join(TFTP_PATH, "config.text"), 
              os.path.join(path, "config.text"))
    # os.system(f'bash move.sh {os.path.join(SFTP_PATH, "config.text")} {os.path.join(path, "config.text")}')
    # os.system(f'bash move.sh config.text {os.path.join(path, "config.text")}')
    return 1

def move_file(old_path, new_path):
    if sys.platform == 'win32':
        command = f'move.bat {old_path} {new_path}'
    else:
        command = f'bash move.sh {old_path} {new_path}'
    return os.system(command)

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
            print('#############################')
            print(f'Connecting to {device[0]}...')
            get_backup_files(*device)
        except SSHConnectionException as e:
            e = int(str(e))
            if e == -128:
                print("\n\n> Exit forced by user.")
                break
            elif e == -64:
                err_string = "TIMEOUT"
            elif e == -32:
                err_string = "WRONG PORT"
            elif e == -16:
                err_string = "AUTH ERROR"
            elif e == -8:
                err_string = "GENERAL FAILURE"
            else:
                err_string = e
            
            print(f'Connection to {device[0]} terminated with code:', err_string)
            failures[device[0]] = err_string

    with open('failures.txt', 'w') as f:
        for key, value in failures.items():
            f.write(f'{key}: {value}')

if __name__ == '__main__':
    main()