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

    def set_credentials(self, username, password):
        pass

    def establish_connection(self, *args, **kwargs):
        pass

    def get_prompt(self):
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
        self.connection_type = 'ssh'
        self.console = Console(hostname=host, visible=visible_console, bound_device=self)

    def set_credentials(self, username, password):
        setattr(self, 'username', username)
        setattr(self, 'password', password)

    def establish_connection(self, do_check_connection=True, show_console=False):
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

        if show_console:
            self.show_console()

    def get_prompt(self):
        if not self._client:
            return 'not_connected' + ' '
        return self._client.find_prompt() + ' '

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

    def show_console(self):
        self.console.show()

    def hide_console(self):
        self.console.hide()

    def close_connection(self):
        """ Closes the connection. """
        self._client.disconnect()
    

class SerialDevice(Device):

    def __init__(self, port):
        self.port = port

    def send_command(self):
        pass


class Console:

    def __init__(self, hostname, visible, bound_device):
        self.history = []
        self._is_visible = visible
        self._hostname = hostname
        self.bound_device = bound_device

        if self._is_visible:
            self.create_frame()

    def create_frame(self):
        self.frame = ConsoleFrame(self.bound_device, parent=None, title=self._hostname, size=(600, 400))
    
    def show(self):
        self.frame.Show()
    
    def hide(self):
        self.frame.Hide()

    def update(self, message, **kwargs):
        if HISTORY_LIMIT:
            if len(self.history) > HISTORY_LIMIT:
                self.history = self.history[1:]
        self.history.append(message)