import serial
import serial.tools.list_ports
import time


def serial_init():
    ports = serial.tools.list_ports.comports()
    port_index = port_selector(ports)
    return serial.Serial(ports[port_index].name, baudrate=9600, timeout=5)  # open serial port


def port_selector(ports):
    i = 0
    for port in ports:
        print(i, port.description)
        i += 1
    print('Select port: ', end='')
    return int(input())


def read_position(serial_port):
    serial_port.write(b'4')
    print(serial_port.read_until(b'\r'))


def main():
    ser = serial_init()
    # ser.write(b'Y')
    # ser.write(b'C22:00:20:1:1')
    while True:
        read_position(ser)


if __name__ == '__main__':
    main()
