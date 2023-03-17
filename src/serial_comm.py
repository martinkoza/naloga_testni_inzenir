import tomli
import serial
import serial.tools.list_ports
import time


out_format = ''


def load_config(config_file):
    with open(config_file, mode="rb") as f:
        config = tomli.load(f)
    return config


def serial_init(config_file):
    """ Connects to E201
    Args:
        Toml configuration file
    Returns:
        serial_port
    """
    ports_list = list(serial.tools.list_ports.comports())
    for port in ports_list:
        # query each port and connect if description is found
        if f'{config_file["interface"]["VID"]}:{config_file["interface"]["PID"]}' in port.hwid:
            print('Serial connection established')
            return serial.Serial(port.device, baudrate=9600, timeout=5, write_timeout=5)  # open serial port
    raise LookupError('E201 not found!')


def read_position_4(serial_port):
    """ Reads position in default format from given serial port

    Args:
        serial_port: From serial_init()

    Returns:
        position in default format
    """
    # global out_format
    # if out_format is 'CRC':
    serial_port.write(b'Sb')
    serial_port.flush()
        # out_format = 'default'
    serial_port.write(b'4')
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_position_crc(serial_port, format):
    """ Reads position in CRC format from given serial port

    Args:
        serial_port: From serial_init()

    Returns:
        position in CRC format
    """
    global out_format
    # if out_format is not 'CRC':
    serial_port.write(format)
    serial_port.flush()
    serial_port.read_until(b'\r')
        # out_format = 'CRC'

    serial_port.write(b'>')
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_position_deg(serial_port, resolution):
    """ Reads position in degrees from given serial port

    Args:
        serial_port: From serial_init()

    Returns:
        Position in degrees
    """
    pos_crc = read_position_crc(serial_port)
    try:
        pos_deg = int(pos_crc.split(':')[1], 16) * 360 / resolution
        return pos_deg
    except IndexError:
        print(f'Error: {pos_crc}')
        return 0


def write_registers(serial_port, command_to_write, register_address_hex):
    global out_format
    if out_format is not 'default':
        serial_port.write(b'Sb')  # Po ukazu nujno sleep, drugače ne prebere!
        time.sleep(0.5)
        serial_port.flush()
        serial_port.reset_input_buffer()
        serial_port.read_all()
        out_format = 'default'
    # serial_port.reset_input_buffer()
    serial_port.flush()
    serial_port.reset_input_buffer()
    serial_port.inWaiting()
    serial_port.write(f'Ws{command_to_write:03}:{register_address_hex:03}'.encode())
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_registers(serial_port, number_of_registers_to_read, starting_register_address_hex):
    global out_format
    if out_format is not 'default':
        serial_port.write(b'Sb')  # Po ukazu nujno sleep, drugače ne prebere!
        time.sleep(0.5)
        serial_port.flush()
        serial_port.reset_input_buffer()
        serial_port.read_all()
        out_format = 'default'
    # serial_port.reset_input_buffer()
    serial_port.flush()
    serial_port.reset_input_buffer()
    serial_port.inWaiting()
    serial_port.write(f'R{number_of_registers_to_read:02}:{starting_register_address_hex:03}'.encode())
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def main():
    """ Loops something """
    config = load_config(r'config.toml')
    ser = serial_init(config)
    try:
        i = 1
        while True:
            print(i, end=': ')
            default_values = {}
            # print(read_position_deg(ser, config['encoder']['RESOLUTION']))
            # print(read_position_crc(ser, config['encoder']['CRC_FORMAT'].encode()))
            # out = read_registers(ser, 2, 0x7e)

            # prints dac output
            for register in config['direct_access_registers']:
                default_value = read_registers(ser, len(register['address']), int(register['address'][0], 16))
                default_values[register['address'][0]] = default_value
                time.sleep(0.1)
            i += 1
            print(default_values)
            break
            # time.sleep(0.5)
    finally:
        ser.close()
        print('Port closed')


if __name__ == '__main__':
    main()
