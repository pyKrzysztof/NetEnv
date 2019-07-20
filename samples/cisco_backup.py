import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netenv.cisco import SSHDeviceCisco
from netenv.codes import error_as_string


TFTP_IP = "192.168.10.1"
ADDRESS = "192.168.10.123"
PORT = 22


def main():
    # Defining the device and passing credentials.
    device = SSHDeviceCisco(ADDRESS, PORT)
    device.set_credentials("admin", "ninja123")

    # Connecting to the device with 15 seconds timeout.
    try: device.connect(timeout=15, raise_on_exception=True)
    except Exception as e: 
        print(error_as_string(e))
        sys.exit()
    else: print("Connected.")

    # Copying the vlan.dat file to the TFTP server.
    try:
        command = f"copy flash:vlan.dat tftp://{TFTP_IP}/vlan.dat"
        out = device.send_command(command, raise_on_exception=True)
        out += device.send_command("\n")
        out += device.send_command("\n")
        out += device.send_command("\n")
    except Exception as e:
        print(out)
        print(error_as_string(e))
    else:
        print("Copied the vlan.dat")

    # Copying the config.text file to the TFTP server.
    try:
        command = f"copy flash:config.text tftp://{TFTP_IP}/config.text"
        out = device.send_command(command, raise_on_exception=True)
        out += device.send_command("\n")
        out += device.send_command("\n")
        out += device.send_command("\n")
    except Exception as e:
        print(out)
        print(error_as_string(e))
    else:
        print("Copied the config.text.")

    # Closing the connection. (Even if it doesn't actually do anything)
    device.close()


if __name__ == "__main__":
    main()