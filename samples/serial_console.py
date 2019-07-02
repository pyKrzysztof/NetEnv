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

# import serial
# import sys
# import time

# class Credentials:

#     username = 'cisco'
#     password = 'class'

#     def __init__(self):
#         pass


# READ_TIMEOUT = 8


# def main():

#     credentials = Credentials()

#     print("\nInitializing serial connection")

    # console = serial.Serial(
    #     port='/dev/ttyUSB0',
    #     baudrate=9600,
    #     parity="N",
    #     stopbits=1,
    #     bytesize=8,
    #     timeout=READ_TIMEOUT
    # )

#     if not console.isOpen():
#         print('port was not opened.')
#         sys.exit()
#     print('port was opened')
#     time.sleep(2)
#     console.write(b"\n\n")
#     time.sleep(1)
#     input_data = console.read(console.inWaiting())
#     print(input_data)
#     if b'Username' in input_data:
#         print('username prompt')
#         console.write(credentials.username + '\r\n')
#     time.sleep(1)
#     input_data = console.read(console.inWaiting())
#     if b'Password' in input_data:
#         print('password prompt')
#         console.write(credentials.password + '\r\n')
#     time.sleep(1)
#     input_data = console.read(console.inWaiting())
#     print(input_data)


# if __name__ == "__main__":
#     main()

# import serial
# import sys
# import time

# previous = None

# def enterdata():
#     global previous
#     ser = serial.Serial('/dev/ttyUSB0', 9600)
#     scom = input()
#     incli = str(scom)
#     ser.write(bytes(f'{incli}\r\n', 'utf-8'))
#     time.sleep(0.5)
#     while True:
#         data = ser.read(ser.inWaiting())
#         if previous == data:
#             continue
#         if (len(data) > 0):
#             print(data.decode('utf-8'))
#             break
#         previous = data
#     ser.close()
#     enterdata()

# enterdata()


import serial
import sys
import time

READ_TIMEOUT = 8

def send(ser, command):
    ser.write(command.encode('utf-8'))
    time.sleep(0.5)
    data = ser.read(ser.inWaiting()).decode('utf-8')
    return data


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity="N",
    stopbits=1,
    bytesize=8,
    timeout=READ_TIMEOUT
)

if not ser.isOpen():
    sys.exit()

print(send(ser, '\n'))
# print(send(ser, 'enable'))
# print(send(ser, 'config terminal'))
# print(send(ser, 'hostname R2'))