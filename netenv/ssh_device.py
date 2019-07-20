import paramiko
import socket
import time

from concurrent.futures import ProcessPoolExecutor
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
		with ProcessPoolExecutor() as p:
			call = p.submit(self._connect)
			try:
				code = call.result(timeout=timeout)
			except TimeoutError:
				code = TIMEOUT_ERROR
			if do_raise_on_exception:
				raise ConnectionException(code)
			return code

	def _connect(self):
		addr, port, un, pw = self.address, self.port, self._un, self._pw
		while True:
			try:
				self._get_client.connect(
					hostname=addr,
					port=port,
					username=un,
					password=pw
				)
			except paramiko.AuthenticationException:
				return AUTH_ERROR
			except socket.error:
				return HOST_UNREACHABLE
			except paramiko.SSHException:
				return GENERAL_FAILURE
			else:
				return 1

	@property
	def address(self):
		return self._address

	@property
	def port(self):
		return self._port

	@property
	def _get_client(self):
		return self._client