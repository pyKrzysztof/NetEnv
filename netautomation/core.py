from paramiko import SSHClient

from .pyping_core import ping


class SSHDevice:

    def __init__(self, host):
        self.host = host
        self.port = 22
        self.connection_type = 'ssh'
        self.username = None
        self.password = None
        self._client = None

    def check_connection(self, timeout=100, count=2):
        """ Returns 1 if connection can be established, 0 otherwise. It uses IMCP. """
        ping_successful = ping(self.host, timeout=timeout, count=count).ret_code == 0
        return ping_successful

    def establish_connection(self, username, password, do_check_connection=True):
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
        self._client.connect(self.host, port=self.port, username=username, password=password)


    def close_connection():
        self._client.close()
    
    def _send_command(self, command):
        """ Sends given command over SSH. """
        if not self._client:
            return 0

        stdin, stdout, stderr = self._client.exec_command(command)
        # handle that.
