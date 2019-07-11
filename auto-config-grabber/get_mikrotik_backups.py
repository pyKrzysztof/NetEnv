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

PATH = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), 'files'), 'mikrotik'))

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

def get_filenames(*args):
    addr, port, username, password = args
    device = SSHDevice(addr, port)
    device.set_credentials(username, password)
    is_ok = device.connect(single_attempt=True)
    if not is_ok:
        raise SSHConnectionException(device.status)
    out = device.send_command('file print detail where type="backup"')
    temp_devices = [entry.replace('\r\n', '', -1) for entry in out.split('\r\n\r\n') if entry]
    devices = [device.split()[1:] for device in temp_devices]
    return devices

def get_latest_backup(filenames, args):

    # getting the dates
    top_time_val = None
    top_idx = None
    for idx, entry in enumerate(filenames):
        combined_date_string = entry[3].split('=')[1].title() + '-' + entry[4]
        time_object = datetime.datetime.strptime(combined_date_string, '%b/%d/%Y-%H:%M:%S')
        if not top_time_val:
            top_time_val = time_object
            top_idx = idx
            continue
        
        if time_object > top_time_val:
            top_time_val = time_object
            top_idx = idx
    try:
        filename = filenames[top_idx][0].split('=')[1].replace('"', '', -1)
    except:
        return None
    else:
        return filename

def get_backup_file(*args):
    target_file = None
    t = 0
    while not target_file:
        t += 1
        filenames = get_filenames(*args)
        target_file = get_latest_backup(filenames, args)
        if target_file is not None:
            break
        if t > 20:
            raise

    path = create_files(args[0])
    new_path = os.path.abspath(os.path.join(path, target_file))
    # print(new_path)
    command = f'bash get_mikrotik_file.sh {args[0]} {args[1]} {args[2]} {args[3]} {target_file} {new_path}'
    print(os.system(command))
    
    return 1

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
            get_backup_file(*device)
        except Exception as e:
            raise
            failures[device[0]] = e
    with open('failures.txt', 'w') as f:
        for key, value in failures.items():
            f.write(f'{key}: {value}')

if __name__ == '__main__':
    main()