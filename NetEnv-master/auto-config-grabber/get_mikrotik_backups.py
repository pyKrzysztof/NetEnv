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


FILE_FAILURE = -256
EXPORT_ITER_TIMEOUT = 15000


class SSHConnectionException(Exception):
    pass

class TimeOutException(Exception):
    pass

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.abspath("C:/users/dude/Documents/DEV-backup/mikrotik")

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
    #devices = resolve_filename_conflicts(devices)
    return devices

#def resolve_filename_conflicts(devices):
#    new_devices = devices
#    print(devices)
#    for device in devices:
#        new_name = ""
#        for index, item in enumerate(device[2:]):
#            if '=' in item:
#                next_eq_sign = index+2
#                break
#        for item in device[1:next_eq_sign]:
#            new_name = new_name + " " + item
#        new_entry = [new_name, *device[next_eq_sign:]]
#        new_devices.append(new_entry)
#        print(device)
#    return new_devices

def get_latest_backup(filenames, args):
    top_time_val = None
    top_idx = None
    for idx, entry in enumerate(filenames):
        print(entry)
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
        try:
            target_file = get_latest_backup(filenames, args)
        except:
            raise SSHConnectionException(FILE_FAILURE)
        if target_file is not None:
            break
        if t > 30:
            raise SSHConnectionException(-64)

    path = create_files(args[0])
    new_path = os.path.abspath(os.path.join(path, target_file))

    print(target_file)
    command = get_script(True, target_file)
    target_file, new_path = fix_path(target_file, new_path)
    command += f"{args[0]} {args[1]} {args[2]} {args[3]} {target_file} {new_path}"
    os.system(command)

    with open(os.path.join(path, 'export.txt'), 'w') as f:
        config = export_config(*args)
        f.write(config)
        print('Exported Config.')
    return 1

def fix_path(target_file, new_path):
    if not "/" in target_file:
        return target_file, new_path
    sl_index = target_file.find("/")
    new_target_file = target_file[sl_index+1:]
    os.makedirs(new_path)
    #print("TARGET FILE:##########################")
    #print(target_file)
    #print("NEW TARGET FILE: #########################")
    #print(new_target_file)
    #print("NEW PATH: ###############################")
    #print(new_path)
    return new_target_file, new_path

def get_script(win_script_file=False, target=None):
    if sys.platform == 'win32':
        if not win_script_file:
            command = os.path.join(THIS_PATH, 'get_mikrotik_file.bat') + " "
        else:
            with open(os.path.join(THIS_PATH, 'script.txt'), 'w') as script:
                script.write(f'get {target}\nbye')
            command = os.path.join(THIS_PATH, 'win_scripted_get_mt_file.bat') + " "
    else:
        command = 'bash get_mikrotik_file.sh '
    return command

def export_config(*args):
    addr, port, username, password = args
    device = SSHDevice(addr, port)
    device.set_credentials(username, password)
    is_ok = device.connect(single_attempt=True)
    if not is_ok:
        raise SSHConnectionException(device.status)
    out = device.send_command('export', iter_timeout=EXPORT_ITER_TIMEOUT)
    return out

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
            print('#############################')
            print(f'Connecting to {device[0]}...')
            get_backup_file(*device)
        except SSHConnectionException as e:
            e = str(e)
            if e == str(-256):
                err_string = "NO BACKUP FILE OR WHITESPACE IN FILENAME"
            elif e == str(-128):
                print("\n\n> Exit forced by user.")
                break
            elif e == str(-64):
                err_string = "TIMEOUT"
            elif e == str(-32):
                err_string = "WRONG PORT"
            elif e == str(-16):
                err_string = "AUTH ERROR"
            elif e == str(-8):
                err_string = "GENERAL FAILURE"
            else:
                err_string = e
            
            print(f'Connection to {device[0]} terminated with code:', err_string)
            failures[device[0]] = err_string
        except Exception as e:
            failures[device[0]] = e
            continue
            

    with open(os.path.join(PATH, 'failures.txt'), 'w') as f:
        for key, value in failures.items():
            f.write(f'{key}: {value}\n')

if __name__ == '__main__':
    main()