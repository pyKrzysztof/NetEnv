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
    device = SSHDeviceCisco(ADDRESS, PORT)
    device.set_credentials("admin", "ninja321")
    code = device.connect(timeout=2)
    if code != 1:
        print(error_as_string(code))
        sys.exit()
    print("Connected.")
    
    success = device.send_command(f"copy flash:vlan.dat tftp://{TFTP_IP}/vlan.dat")
    if success != 1:
        print(error_as_string(success))
    device.send_command("\n")
    device.send_command("\n")
    device.send_command("\n")
    print("Copied the vlan.dat")

    success = device.send_command(f"copy flash:config.text tftp://{TFTP_IP}/config.text")
    if success != 1:
        print(error_as_string(success))
        device.close()
        sys.exit()
    device.send_command("\n")
    device.send_command("\n")
    device.send_command("\n")
    print("Copied the config.text.")

    device.close()


if __name__ == "__main__":
    main()