import netmiko
import serial
import json
import time
import sys

ATTEMPTS = 10

class CredentialsNotProvided(Exception):
    pass

class DeviceNotBoundException(Exception):
    pass

class NotImplementedYet(Exception):
    pass

class Device:
    
    def __init__(self, host):
        self.host = host

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def set_device_type(self, device_type):
        self.device_type = device_type

    def establish_connection(self):
        pass

    def get_prompt(self):
        pass

    def send_command(self, command):
        pass

    def enter_conft(self):
        pass

    def exit_conft(self):
        pass

    def close_connection(self):
        pass

class SSHDevice(Device):

    def establish_connection(self):
        host = self.host
        un = getattr(self, 'username', 'cisco')
        pd = getattr(self, 'password', 'class')
        dt = getattr(self, 'device_type', 'cisco_ios')
        self.client = netmiko.ConnectHandler(host=host, username=un, 
                                             password=pd, device_type=dt)
    
    def send_command(self, command=None, config=False):
        if not command:
            return
        if config:
            return self.client.send_config_set(command)
        if not config:
            return self.client.send_command(command)

    def get_prompt(self):
        return self.client.find_prompt()

    def close_connection(self):
        self.client.disconnect()

class SerialDevice:

    def __init__(self, port, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=8):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
    
    def serial_protocol_config(self):
        platform = sys.platform
        if platform == 'win32':
            return
        self.serial.setDTR(True)
        self.serial.setRTS(False)

    def set_credentials(self, username, password):
        self._username = username
        self._password = password

    def get_credentials(self):
        if not hasattr(self, '_username') and not hasattr(self, '_password'):
            raise CredentialsNotProvided
        return self._username, self._password

    def _login(self):
        un, pd = self.get_credentials()
        for _ in range(ATTEMPTS):
            command = '\r\n'.encode('utf-8')
            self.serial.write(command)
            time.sleep(.5)
            out = self.serial.read(self.serial.inWaiting()).decode('utf-8', 'ignore')
            if not out.strip().endswith('Username:'):
                continue
            self.serial.write(f'{un}\n'.encode('utf-8'))
            time.sleep(.5)
            out = self.serial.read(self.serial.inWaiting()).decode('utf-8', 'ignore')
            if not out.strip().endswith('Password:'):
                continue
            self.serial.write(f'{pd}\n'.encode('utf-8'))
            time.sleep(.5)
            out = self.serial.read(self.serial.inWaiting()).decode('utf-8', 'ignore')
            return 1
        return 0

    def _is_logged_in(self, output=None):
        if not output:
            self.write('', new_line=False)
            output = self.read()
        if '>' in output or '#' in output:
            return 1
        return 0

    def connect(self):
        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize,
            timeout=self.timeout
        )
        self.serial_protocol_config()

        is_open = self.serial.isOpen()
        if not is_open:
            sys.exit()

        self.serial.flushInput()

        for _ in range(5):
            self.write('\r\n', new_line=False)
            time.sleep(.5)
            out = self.read()
            if self._is_logged_in(out):
                return 1
            if out.endswith('Username:'):
                return self._login()

        if self._is_logged_in():
            return 1
        return 0

    def send_command(self, command, new_line=True, delay=0.5, do_print=True):
        self.write(command, new_line)
        time.sleep(delay)
        out = self.read().replace(command, '')
        if do_print:
            print(out)
        return out

    def read(self):
        out = self.serial.read(self.serial.inWaiting()).decode('utf-8', 'ignore')
        return out #NOTE I removed the .strip() from here, if something doesn't work. that's the reason!

    def write(self, command, new_line):
        if new_line:
            command = f'{command}\n'
        command = command.encode('utf-8')
        self.serial.write(command)

class SSHCommandHandler:

    """ 
    Handles the commands and automation. 
    Levels are:
    0 - (unaccessable, raises an exception.)
    1 - (privilaged mode (enable))
    2 - (configuration mode (conf t))
    3 - (sub conf t)
    """

    level = 1
    device = None
    
    def __init__(self, automation_file_path=None):
        self.automation_handler = AutomationHandler()
        if not automation_file_path:
            return
        self.automation_handler.set_file(automation_file_path)

    def bind_device(self, device):
        self.device = device

    def set_level(self, level):
        self.level = level

    def translate(self, message):
        # translate message into command / commands here.
        message = message.strip()
        enter_conf_t = message == 'conf t' or \
                       message == 'configure terminal' or \
                       message == 'configure t' or \
                       message == 'conf term' or \
                       message == 'config term'
        if enter_conf_t:
            return ('-1', )
        if message.startswith('>'):
            commands = self.automation_handler.translate(message[1:])
            return commands
        return [message, ] 
        

    def execute_commands(self, commands):
        # pass all commands to device.
        try:
            commands, level = commands
            if int(level) == 2:
                return [self.device.send_command(commands, config=True), ]
        except:
            pass
        out = []
        if not commands:
            return ['Wrong command.', ]
        elif commands[0] == '-1':
            return ['Do not enter configuration terminal!\nRun config commands as \'> [command]\' if you must.\nWrite automation.json file, load it and execute commands from there.', ]
        for command in commands:
            out.append(self.device.send_command(command))

        return out

class Handler:
    
    def __init__(self):
        pass

    def bind_device(self, device):
        self.device = device

    def execute(self, command):
        if command.startswith('!'):
            return self.handle_auto_command(command[1:])
        return self.handle_regular_command(command)

    def handle_regular_command(self, command, ):
        if not hasattr(self, 'device'):
            raise DeviceNotBoundException
        out = self.device.send_command(command, new_line=True, do_print=False)
        if 'show' in command:
            for _ in range(10):
                if out.strip().endswith('--More--'):
                    out = out.replace(' --More--', '')
                    temp = self.device.send_command(' ', new_line=False, do_print=False, delay=.1)
                    out += temp
                    # Next result is wrongly formatted (ALWAYS), you can later find '\r\n' in previous line
                    # and from that calculate accurate indices from current space. (This is true for show ip int br)
                temp = self.device.send_command('', new_line=False, do_print=False, delay=.5)
                if temp.strip().endswith('--More--'):
                    temp = temp.replace(' --More--', '')
                    out += temp
                    temp = self.device.send_command(' ', new_line=False, do_print=False, delay=.1)
                    # Next result is wrongly formatted (ALWAYS), you can later find '\r\n' in previous line
                    # and from that calculate accurate indices from current space. (This is true for show ip int br)
                out += temp
        return out

    def handle_auto_command(self, command):
        raise NotImplementedYet

class AutomationHandler:

    commands = None

    def __init__(self):
        pass

    def set_file(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.proccess_data(data)

    def proccess_data(self, data):
        self.commands = data

    def translate(self, command):
        # command ->  "<command> <param1> <param2>"
        found = False
        for comm in self.commands:
            if comm in command:
                parameters = command[len(comm)+1:].split()
                found = True
                break
        if not found:
            return ([command, ], '2')
        if not len(parameters) == len(self.commands[comm]['parameters']):
            return
        mod_commands = []
        parameters = list(zip(self.commands[comm]['parameters'], parameters))
        for command in self.commands[comm]['commands']:
            mod_command = command
            for name, value in parameters:
                mod_command = mod_command.replace(f'|{name}|', value, -1)
            
            mod_commands.append(mod_command)
        return (mod_commands, self.commands[comm]['level'])
