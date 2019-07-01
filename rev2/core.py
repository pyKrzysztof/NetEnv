import netmiko
import serial
import json


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

    def enter_conft(self):
        pass

    def exit_conft(self):
        pass

    def get_prompt(self):
        return self.client.find_prompt()

    def close_connection(self):
        self.client.disconnect()


class SerialDevice(Device):
    
    def __init__(self, port):
        self.port = port

    def establish_connection(self):
        try:
            self.client = serial.serial_for_url(url=self.port)
            if self.client.isOpen():
                return True
        except:
            raise
            return False
    
    def _read_serial(self):
        data_bytes = self.client.inWaiting()
        if data_bytes:
            return self.client.read(data_bytes)
        return ''

    def _write_serial(self, command):
        self.client.write(command + '\n')

    def get_prompt(self):
        return 'not implemented yet#'

    def send_command(self, command=None):
        if not command:
            return
        self._write_serial(command)
        return self._read_serial()


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

class SerialCommandHandler(SSHCommandHandler):

    def translate(self, message):
        if message.startswith('>'):
            commands = self.automation_handler.translate(message[1:])
            return commands
        return [message, ]

    def execute_commands(self, commands):
        # pass all commands to device.
        try:
            commands, level = commands
            if int(level) == 2:
                self.device.send_command('conf t')
        except:
            pass
        out = []
        if not commands:
            return ['Wrong command.', ]
        elif commands[0] == '-1':
            return ['Do not enter configuration terminal!\nRun config commands as \'> [command]\' if you must.\nWrite automation.json file, load it and execute commands from there.', ]
        for command in commands:
            out.append(self.device.send_command(command))

        try:    
            if int(level) == 2:    
                self.device.send_command('end')
        except:    
            pass

        return out



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