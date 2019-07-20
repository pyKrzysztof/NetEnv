import multiprocessing
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
        do_raise_on_exception = kwargs.get("raise_on_exception", False)
        timeout = kwargs.get("timeout", 30)
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=self._send_shell_command, args=[self._shell, command, return_dict])
        p.start()
        p.join(timeout)
        if p.is_alive():
            p.terminate()
            p.join()
            code = TIMEOUT_ERROR
        else:
            code = return_dict["exit_code"]
        if do_raise_on_exception:
            raise ConnectionException(code)
        return code

    def _send_shell_command(self, shell, command, return_dict):
        try:
            shell.send(command)
            shell.send("\n")
            time.sleep(0.5)
            out = ""
            while not self._shell.exit_status_ready():
                rl, _, _ = select.select([self._shell], [], [], 0)
                if len(rl) > 0:
                    out += self._shell.recv(1024).decode("utf-8")
            return_dict["output"] = out
            return
        except paramiko.SSHException:
            code = CHANNEL_FAILURE
        except:
            code = GENERAL_FAILURE
        return_dict["exit_code"] = code

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
