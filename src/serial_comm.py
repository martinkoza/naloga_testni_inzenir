import tomli
import serial
import serial.tools.list_ports
import time


out_format = ''


def load_config(config_file):
    # TODO: docstring
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
    global out_format
    if out_format is not 'default':
        # TODO: določi minimalen čas sleep-a
        serial_port.write(b'Sb')  # Po ukazu nujno sleep, drugače ne prebere!
        time.sleep(0.5)
        serial_port.flush()
        serial_port.reset_input_buffer()
        serial_port.read_all()
        out_format = 'default'
    serial_port.write(b'4')
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_position_formatted(serial_port):
    # TODO: kako se sploh reče temu formatu???
    """ Reads position in CRC format from given serial port

    Args:
        serial_port: From serial_init()

    Returns:
        position in multiturn:singleturn:warning:error format
    """
    global out_format
    if out_format is not 'formatted':
        serial_port.write(b'C22:00:20:1:1')  # Po ukazu nujno sleep, drugače ne prebere!
        time.sleep(0.5)
        serial_port.flush()
        serial_port.reset_input_buffer()
        serial_port.read_all()
        out_format = 'formatted'
    serial_port.write(b'>')
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_position_crc(serial_port):
    # TODO: kako se sploh reče temu formatu???
    """ Reads position in CRC format from given serial port

    Args:
        serial_port: From serial_init()

    Returns:
        position in CRC format
    """
    global out_format
    if out_format is not 'formatted':
        serial_port.write(b'C22:00:20:1:1')  # Po ukazu nujno sleep, drugače ne prebere!
        time.sleep(0.5)
        serial_port.flush()
        serial_port.reset_input_buffer()
        serial_port.read_all()
        out_format = 'formatted'
    serial_port.write(b'4')
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_position_deg(serial_port, resolution):
    """ Reads position in degrees from given serial port

    Args:
        serial_port: From serial_init()
        resolution: encoder resolution

    Returns:
        Position in degrees
    """
    global out_format
    if out_format is not 'CRC':
        serial_port.write(b'Sb')  # Po ukazu nujno sleep, drugače ne prebere!
        time.sleep(0.5)
        serial_port.flush()
        serial_port.reset_input_buffer()
        serial_port.read_all()
        out_format = 'default'
    pos_crc = read_position_formatted(serial_port)
    try:
        pos_deg = int(pos_crc.split(':')[1], 16) * 360 / resolution
        return pos_deg
    except IndexError:
        print(f'Error: {pos_crc}')
        return 0


def write_registers(serial_port, command_to_write, register_address_hex):
    # TODO: docstring
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


def send_command(command, serial_port):
    # TODO: docstring
    """ Sends command string to serial port

    Args:
        command: Custom write string to send
        serial_port: From serial_init()

    Returns:
        Reply from serial
    """
    serial_port.flush()
    serial_port.reset_input_buffer()
    serial_port.inWaiting()
    serial_port.write(command.encode())
    serial_port.flush()
    return serial_port.read_until(b'\r').decode('utf-8')


def read_registers(serial_port, number_of_registers_to_read, starting_register_address_hex):
    # TODO: docstring
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


def calculate_ride_height(serial_port):
    pass


def crc_remainder(input_bitstring, polynomial_bitstring, initial_filler):
    # TODO: docstring
    # Shamelessly stolen from wikipedia
    """ Calculate the CRC remainder of a string of bits using a chosen polynomial.
    initial_filler should be '1' or '0'.
    """
    polynomial_bitstring = polynomial_bitstring.lstrip('0')  # remove leading zeroes of polynomial
    len_input = len(input_bitstring)
    initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ''.join(input_padded_array)[len_input:]


def crc_check(input_bitstring, polynomial_bitstring, check_value):
    # TODO: docstring
    """Calculate the CRC check of a string of bits using a chosen polynomial.

    """
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = check_value
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ''.join(input_padded_array)[len_input:]


def main():
    """ Loops something """
    config = load_config(r'../config.toml')
    ser = serial_init(config)
    try:
        send_command('Y', ser)
        send_command('X', ser)
        i = 1
        while True:
            print(i, end=': ')
            default_values = {}
            # print(read_position_deg(ser, config['encoder']['RESOLUTION']))
            # print(read_position_formatted()(ser, config['encoder']['CRC_FORMAT'].encode()))
            # out = read_registers(ser, 2, 0x7e)

            # prints dac output
            print(read_position_crc(ser))
            time.sleep(0.5)
            print(read_position_formatted(ser))
            i += 1
            # print(send_command('K', ser))

            # break
            time.sleep(2)
    finally:
        ser.close()
        print('Port closed')


if __name__ == '__main__':
    main()
