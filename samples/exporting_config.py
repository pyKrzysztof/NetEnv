import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netenv import SSHDevice
from netenv.codes import error_as_string


ADDRESS = "192.168.10.123"
PORT = 22


def main():
	device = SSHDevice(ADDRESS, PORT)
	device.set_credentials("admin", "ninja123")
	result = device.connect(timeout=2, raise_on_exception=False)
	if result != 1:
		print(error_as_string(result))
		sys.exit()
	config = device.send_command("export")
	device.close()
	with open("export", "w") as f:
		f.write(config)


if __name__ == "__main__":
	main()
