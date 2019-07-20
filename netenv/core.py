

class ConnectionException(Exception):
    pass


class Device:

    def __init__(self):
        pass

    def set_credentials(self, username, password):
        """
        Sets credentials, alternatively specify
        them when connecting to the device.
        """
        pass

    def connect(self, **kwargs):
        """Specify connection parameters."""
        pass

    def send_command(self, command, **kwargs):
        """
        Sends a command to the device,
        additional keyword arguments are device specific.
        """
        pass

    def close(self):
        """Closes the connection."""
        pass


class CommandPipe:

    def __init__(self, *args, **kwargs):
        """You can bind device, and add commands here or later."""
        self.args = args
        for key, value in kwargs.items():
            setattr(self, key, value)

    def bind_device(self, device):
        """Bind this pipe to the device."""
        pass

    def add_command(self, command, on_error):
        """Specify the command and what to the on error."""
        pass

    def exec_commands(self, verbose):
        """
        Executes all bound commands except 
        when 'on_error' specifies not to.
        """
        pass

    def get_full_raport(self):
        """
        Returns a string of all ran commands 
        and corresponding responses from the device.
        """
        pass
