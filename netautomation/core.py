import netmiko

from .pyping_core import ping
from .gui import ConsoleFrame

HISTORY_LIMIT = 60


class Device:

    username = ''
    password = ''
    device_type = 'cisco_ios'


    def check_connection(self, *args, **kwargs):
        """ 
        Returns 1 if connection can be established, 0 otherwise. It uses IMCP.
        Keyword arguments are:
        - timeout [ms],
        - count [int] 
        """
        ping_successful = ping(self.host, timeout=kwargs.get('timeout', 150), count=kwargs.get('count', 2)).ret_code == 0
        return ping_successful

    def establish_connection(self, *args, **kwargs):
        pass

    def close_connection(self):
        pass

    def send_command(self):
        pass
    


class SSHDevice(Device):

    def __init__(self, host, visible_console=True):
        self.host = host
        self.port = 22
        self._client = None
        self._logger = Logger()
        self.connection_type = 'ssh'
        self.console = Console(hostname=host, visible=visible_console)

    def set_credentials(self, username, password):
        setattr(self, 'username', username)
        setattr(self, 'password', password)

    def establish_connection(self, do_check_connection=True):
        """
        Establishes connection with the device over ssh, if user credentials match.
        if you are using higher level API,  do_check_connection  should be set to False and be handled
        by your solution. (As in sample GUI)
        """
        if do_check_connection:
            response = self.check_connection()
            if not response:
                return 0

        self._client = netmiko.ConnectHandler(host=self.host, port=self.port, 
                                              username=self.username, password=self.password, 
                                              device_type=self.device_type)

    def close_connection(self):
        """ Closes the connection. """
        self._client.disconnect()
    
    def send_command(self, commands, level=''):
        """ 
        Sends given command over SSH.
        levels: 'conft-enter', 'conft-exit'.
        """
        if not self._client:
            return 0
        if level == 'conft-enter':
            self._client.send_command('conf t')
        out = self._client.send_command(commands)
        if level == 'conft-quit':
            self._client.send_command('exit')
        self._logger.log(out)


class SerialDevice(Device):

    def __init__(self, port):
        self.port = port

    def send_command(self):
        pass

class Logger:

    def __init__(self):
        self._log = []

    def log(self, out):
        self._log.append(out)



class Console:

    def __init__(self, hostname, visible):
        self.history = []
        self._is_visible = visible
        self._hostname = hostname

        if self._is_visible:
            self.create_frame()

    def create_frame(self):
        self.frame = ConsoleFrame(None, title=self._hostname, size=(600, 400))
        self.frame.Show()
    
    def update(self, message, **kwargs):
        if HISTORY_LIMIT:
            if len(self.history) > HISTORY_LIMIT:
                self.history = self.history[1:]
        self.history.append(message)

