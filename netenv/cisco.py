import paramiko
import socket
import select
import time

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures._base import TimeoutError

from .core import ConnectionException
from .ssh_device import SSHDevice
from .serial_device import SerialDevice
from .codes import *


class SSHDeviceCisco(SSHDevice):

    def __init__(self, address=None, port=None):
        super().__init__(address, port)

    def send_command(self, command, **kwargs):
        if getattr(self, "_is_shell_invoked", False):
            self._invoke_shell()
        timeout = kwargs.get("timeout", 15)
        with ProcessPoolExecutor() as p:
            call = p.submit(self._send_shell_command, [self._shell, command])
            try: 
                out = call.result(timeout=timeout)
            except TimeoutError:
                code = TIMEOUT_ERROR
            except paramiko.SSHException:
                code = CHANNEL_FAILURE
            except:
                code = GENERAL_FAILURE
            else:
                return out
            if kwargs.get("raise_on_exception", False):
                raise ConnectionException(out)
            return code

    def _invoke_shell(self):
        self._shell = self._get_client.invoke_shell()
        setattr(self, "_shell_invoked", True)
        if not self._paging_of(self._shell):
            raise ConnectionException(CHANNEL_FAILURE)

    def _paging_of(self, shell):
        try:
            shell.send("terminal length 0\n")
            time.sleep(1)
            shell.recv(9999)
        except:
            return 0
        else:
            return 1

    def _send_shell_command(self, shell, command):
        shell.send(command)
        shell.send("\n")
        time.sleep(0.5)
        out = ""
        while not self._shell.exit_status_ready():
            rl, _, _ = select.select([self._shell], [], [], 0)
            if len(rl) > 0:
                out += self._shell.recv(1024).decode("utf-8")
        return out
