import serial
import serial.tools.list_ports
import time


# E201 Encoder interface:
# https://www.rls.si/eng/fileuploader/download/download/?d=1&file=custom%2Fupload%2FE201D01_07_bookmark.pdf
VID = '0483'
PID = '5740'

# Encoder
RESOLUTION = 2**20


out_format = 'default'

# TODO: dodaj komentarje - https://google.github.io/styleguide/pyguide.html


def serial_init():
    ports_list = list(serial.tools.list_ports.comports())
    for port in ports_list:
        # query each port and connect if description is found
        if f'{VID}:{PID}' in port.hwid:
            # return serial.Serial(ports_list[port_index].name, baudrate=9600, timeout=5, write_timeout=5)
            # TODO: Preveri če dela spodnji return tudi za windows (zgornji za linux ne deluje)
            print('Serial connection established')
            return serial.Serial(port.device, baudrate=9600, timeout=5,
                                 write_timeout=5)  # open serial port
    raise LookupError('E201 not found!')


def read_position_4(serial_port):
    """ returns position in default format"""
    global out_format
    if out_format is 'CRC':
        serial_port.write(b'Sb')
        serial_port.flush()
        out_format = 'default'
    serial_port.write(b'4')
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_position_crc(serial_port):
    """ returns position in crc format"""
    global out_format
    if out_format is not 'CRC':
        # serial_port.write(b'Y')   # Ne opazim nobene razlike z in brez komande Y (ali X)
        # serial_port.flush()
        serial_port.write(b'C22:00:20:1:1')
        serial_port.flush()
        out_format = 'CRC'
    serial_port.write(b'>')
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_position_deg(serial_port):
    pos_crc = read_position_crc(serial_port)
    try:
        pos_deg = int(pos_crc.split(':')[1], 16) * 360 / RESOLUTION
        return pos_deg
    except IndexError:
        print(f'Error: {pos_crc}')
        return 0


def main():
    ser = serial_init()
    try:
        i = 1
        while True:
            print(i, end=': ')
            # print(read_position_deg(ser))
            print(read_position_crc(ser))
            i += 1
            time.sleep(0.5)
    finally:
        ser.close()
        print('Port closed')


if __name__ == '__main__':
    main()
