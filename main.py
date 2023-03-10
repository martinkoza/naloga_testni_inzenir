import pytest
import serial
import serial.tools.list_ports
import time
import keyboard


def test_position_for_error():
    """
    preverjanje pravilnega branja pozicije
    """
    ser = serial_init()
    # for i in range(20):
    #     assert read_position_crc(ser) != -1


def serial_init(port=None):
    ports_list = serial.tools.list_ports.comports()  # list available ports
    if port is None:
        port_index = port_selector(ports_list)
    else:
        port_index = 0
    return serial.Serial(ports_list[port_index].name, baudrate=9600, timeout=5, write_timeout=5)  # open serial port


def port_selector(ports):
    i = 0
    for port in ports:
        print(i, port.description)
        i += 1
    print('Select port: ', end='')
    return int(input())


def read_position_4(serial_port):
    """ returns position in default format"""
    if format_crc is True:
        serial_port.write(b'Sb')
    serial_port.write(b'4')
    return serial_port.read_until(b'\r').decode('utf-8')


def read_position_crc(ser):
    """ returns position in crc format"""
    if format_crc is False:
        #ser.write(b'Y')
        ser.write(b'C22:00:20:1:1')
    ser.write(b'>')
    return ser.read_until(b'\r').decode('utf-8')


def main():
    ser = serial_init(port=0)
    i = 1
    while True:
        out = read_position_crc(ser)
        try:
            print(out)
            #position = int(out.split(':')[1], 16)
            #print(position)
        except IndexError:
            print(f'Error: {out}')
            # return -1
        if keyboard.is_pressed('c'):
            ser.close()
            break
        print(f'{i}: ', end='')
        i += 1
        if i == 200:
            ser.close()
            break

        time.sleep(0.1)

    print('Done')


format_crc = False

if __name__ == '__main__':
    main()
