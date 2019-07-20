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

BACKUP_PATH = os.path.abspath("C:/users/dude/Documents/DEV-backup")
PATH = os.path.abspath(os.path.dirname(__file__))

def sort_devices_by_type(devices):
    cisco_devices = []
    mt_devices = []
    
    for device in devices:
        device_t = get_device_type(device)
        if not device_t:
            continue
        elif device_t == "mt":
            mt_devices.append(device[1])
        elif device_t == "cisco":
            cisco_devices.append(device[1])
       
    return (cisco_devices, mt_devices)

def get_device_type(device):
    name = device[0]
    if name.startswith("mt") or name.startswith("sxt"):
        return "mt"
    elif name.startswith("cisco"):
        return "cisco"
    return None
    
def get_main_list():
    devices = []
    with open(os.path.join(BACKUP_PATH, 'list.txt'), "r") as f:
        for line in f:
            devices.append(list(line.split()))
    return devices

def write_cisco_list(devices):
    port, usrn, pd = get_credentials_by_type("cisco")
    with open(os.path.join(PATH, "cisco_list.txt"), 'w') as f:
        for device in devices:
            f.write(f"{device} {port} {usrn} {pd}\n")
    
def write_mt_list(devices):
    port, usrn, pd = get_credentials_by_type("mt")
    with open(os.path.join(PATH, "mt_list.txt"), 'w') as f:
        for device in devices:
            f.write(f"{device} {port} {usrn} {pd}\n")
    
def get_credentials_by_type(device_t):
    with open(os.path.join(BACKUP_PATH, f"{device_t}_credentials.txt"), 'r') as f:
        port, usrn, pw = f.read().split(" ")
    return port, usrn, pw
    
def main():
    devices = get_main_list()
    cisco, mt = sort_devices_by_type(devices)
    write_mt_list(mt)
    write_cisco_list(cisco)
    try:
        #os.system("python " + os.path.join(PATH, "get_mikrotik_backups.py"))
        os.system("python " + os.path.join(PATH, "get_cisco_backups.py"))
    except:
        sys.exit()
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    