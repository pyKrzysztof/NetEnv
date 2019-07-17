# NetEnv

Built around paramiko and pySerial.

This library supports:
* Serial Connection,
* SSH Connection.

Each class has the following methods:

- `__init__(*args, **kwargs)`
- `set_credentials(username, password)`
- `get_credentials()`
- `connect(single_attempt=False)`
- `send_command(command)`
- `close()`

### EXAMPLE - Connecting to a MikroTik and exporting it's config:

    device = SSHDevice('192.168.88.1', port=22)
    device.set_credentials(admin, ninjapassword)
    is_connected = device.connect()
    if not is_connected:
        return 0
    
    out = device.send_command('export')
    device.close()

#### NOTE: Some cisco devices do not support sending more than one command per SSH connection. Working on an elegant fix.

### auto-config-grabber Explained
It is a dedicated script I wrote for my boss, it collects vlan.dat and config.text from provided Cisco Switches,
the most recent backups from all listed MikroTik Routers and their 'export' output.
To use:
1) Set up a local tftp server. (On your local machine, where you would use this script.)
2) To both cisco (cisco_list) and mikrotik (mt_list) lists add the information of your devices in the following way:
 `address port username password`
3) run both `get_cisco_backups.py` and `get_mikrotik_backups.py`
