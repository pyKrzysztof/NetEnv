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

    now = datetime.now()
    backup_folder_name = f'{now.day}/{now.month}/{now.year}-{now.hour}:{now.minute}'
    backup_folder_path = os.path.join(path, backup_folder_name)
    os.makedirs(backup_folder_path)
    return backup_folder_path

def get_filenames(*args):
    addr, port, username, password = args
    device = SSHDevice(addr, port)
    device.set_credentials(username, password)
    is_ok = device.connect(single_attempt=True)
    if not is_ok:
        raise SSHConnectionException(device.status)
    out = device.send_command('file print where type="backup"')
    device.send_command('quit')
    return out

def get_latest_backup(filenames):
    data = filenames.split('\n')
    rows = len(data)
    data = [row.split() for row in data]

    # filtering out the first row containing column names
    data = data[1:]

    # filtering out the size,
    data = [(entry[0], entry[1], entry[2], entry[4], entry[5]) for entry in data]

    # index:    0    1      2                3                       4
    # type:    idx, name, type, "str(mon)/int(day)/int(year)", "hr:min:sec" of creation

    # filtering the non-backup files.
    data = [entry for entry in data if entry[2] == 'backup']

    # getting the dates
    top_time_val = None
    top_idx = None
    for idx, entry in enumerate(data):
        combined_date_string = entry[3] + '-' + entry[4]
        time_object = datetime.datetime.strptime(combined_date_string, format='%b/%d/%Y-%h:%m:%s')
        if not top_time_val:
            top_time_val = time_object
            top_idx = idx
            continue
        
        if time_object > top_time_val:
            top_time_val = time_object
            top_idx = idx
    
    filename = data[top_idx][1]
    return filename

def get_backup_file(*args):
    filenames = get_filenames(*args)
    target_file = get_latest_backup(filenames)
    path = create_files(args[0])
    command = ["sshpass", "-f", f"<(printf '%s\n' {args[3]})", "sftp", "-P", f"{args[1]}", f"{args[2]}@{args[0]}:{target_file}"]
    subprocess.run(command)
    command = [f'mv {target_file} {os.path.abspath(os.path.join(path, target_file))}']
    subprocess.run(command)
    return 1

def main():
    failures = {}
    with open('mt_list.txt', 'r') as f:
        data = f.readlines()
        devices = [entry.split() for entry in data]
        for device in devices:
            device[1] = int(device[1])
    for device in devices:
        try:
            get_backup_file(*device)
        except Exception as e:
            failures[device[0]] = e
    with open('failures.txt', 'w') as f:
        for key, value in failures.items():
            f.write(key + ':', value)

if __name__ == '__main__':
    main()
    # args = 'address', 'port', 'username', 'password'
    # target_file = 'test'
    # command = ["sshpass", "-f", f"<(printf '%s\n' {args[3]})", "sftp", "-P", f"{args[1]}", f"{args[2]}@{args[0]}:{target_file}"]
    # print(command)

# sshpass -f <(printf '%s\n' 'test') sftp -P 22 admin@192.168.88.1:MikroTik-11011970-1525.backup