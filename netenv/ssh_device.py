import paramiko
import socket
import time

import multiprocessing
from concurrent.futures._base import TimeoutError

from .core import Device
from .core import ConnectionException
from .codes import *


class SSHDevice(Device):

	def __init__(self, address=None, port=None):
		"""Initializes the device, arguments are address and port."""
		self._address = address
		self._port = int(port)
		self._client = paramiko.SSHClient()
		self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	def set_credentials(self, username, password):
		self._un = username
		self._pw = password

	def connect(self, **kwargs):
		timeout = kwargs.get("timeout", 30)
		do_raise_on_exception = kwargs.get("raise_on_exception", False)
		manager = multiprocessing.Manager()
		return_dict = manager.dict()
		p = multiprocessing.Process(target=self._connect, args=[return_dict])
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

	def close(self):
		self._client.close()

	def _connect(self, return_dict):
		addr, port, un, pw = self.address, self.port, self._un, self._pw
		try:
			self._get_client.connect(
				hostname=addr,
				port=port,
				username=un,
				password=pw
			)
		except paramiko.AuthenticationException:
			code = AUTH_ERROR
		except socket.error:
			code = HOST_UNREACHABLE
		except paramiko.SSHException:
			code = GENERAL_FAILURE
		else:
			code = 1
		finally:
			return_dict["exit_code"] = code
			return code

	@property
	def address(self):
		return self._address

	@property
	def port(self):
		return self._port

	@property
	def _get_client(self):
		return self._client
