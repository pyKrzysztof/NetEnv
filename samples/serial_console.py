# import sys

# from context import *

# from rev2 import SerialDevice
# from rev2 import SerialCommandHandler

# if __name__ == '__main__':
#     # check with 'sudo screen /dev/ttyUSB<n> 9600' or 
#     # '/dev/ttyS<n> 9600' if you have serial interface.
#     device = SerialDevice(port='/dev/ttyUSB1')
#     device.set_credentials('cisco', 'class')

#     handler = SerialCommandHandler('commands.json')
#     handler.bind_device(device)

#     connected = device.establish_connection()
#     if not connected:
#         sys.exit()

#     while True:
#         stdin = input(device.get_prompt() + ' ')
#         commands = handler.translate(stdin)
#         stdout = handler.execute_commands(commands)
#         if not stdout:
#             continue
#         for out in stdout:
#             print(out)

###############################################
# import serial
# import sys

# ser = serial.Serial(
#     port='/dev/ttyUSB1', 
#     baudrate=9600,
#     parity='N',
#     stopbits=1,
#     bytesize=8,
#     timeout=8
# )

# if not ser.isOpen():
#     sys.exit()

# ser.write('\n') # try '\r\n'
# read_bytes = ser.inWaiting()
# print(read_bytes)
# if read_bytes > 0:
#     ser.read(read_bytes)
###############################################

import serial
import sys
import time

class Credentials:

    username = 'cisco'
    password = 'class'

    def __init__(self):
        pass


READ_TIMEOUT = 8


def main():

    credentials = Credentials()

    print("\nInitializing serial connection")

    console = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=READ_TIMEOUT
    )

    if not console.isOpen():
        print('port was not opened.')
        sys.exit()

    console.write("\r\n\r\n")
    time.sleep(1)
    input_data = console.read(console.inWaiting())
    if 'Username' in input_data:
        console.write(credentials.username + '\r\n')
    time.sleep(1)
    input_data = console.read(console.inWaiting())
    if 'Password' in input_data:
        console.write(credentials.password + '\r\n')
    time.sleep(1)
    input_data = console.read(console.inWaiting())
    print(input_data)


if __name__ == "__main__":
    main()