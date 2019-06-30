from paramiko import SSHClient

from .pyping_core import ping


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

    def __init__(self, host):
        self.host = host
        self.port = 22
        self._client = None
        self._logger = Logger()
        self.connection_type = 'ssh'

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

        self._client = SSHClient()
        self._client.load_system_host_keys()
        self._client.connect(self.host, port=self.port, username=self.username, password=self.password)

    def close_connection(self):
        """ Closes the connection. """
        self._client.close()
    
    def send_command(self, command):
        """ Sends given command over SSH. """
        if not self._client:
            return 0

        stdin, stdout, stderr = self._client.exec_command(command)
        self._logger.log(stdin, stdout, stderr)
        return stdin, stdout, stderr


class SerialDevice(Device):

    def __init__(self, port):
        self.port = port

    def send_command(self):
        pass

class Logger:

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.errors = []
        self.count = 0

    def log(self, ins, out, err):
        self.inputs.append(ins)
        self.outputs.append(out)
        self.errrors.append(err)
        self.count += 1