import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netenv import SSHDevice
from netenv.codes import error_as_string


ADDRESS = "192.168.10.123"
PORT = 22


def main():
	# Defining the device and passing the credentials.
	device = SSHDevice(ADDRESS, PORT)
	device.set_credentials("admin", "ninja123")

	# Attempting to connect to the device.
	try: device.connect(timeout=15, raise_on_exception=True)
	except Exception as e: 
		print(error_as_string(e))
		sys.exit()

	# Exporting the config.
	try: config = device.send_command("export", raise_on_exception=True)
	except Exception as e:
		print(error_as_string(e))
		sys.exit()
	else:
		with open("export", "w") as f:
			f.write(config)
		device.close()


if __name__ == "__main__":
	main()
