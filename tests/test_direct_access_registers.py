import pytest
import serial_comm
import re
import tomli
import time

# TODO: komentarji funkcij


def test_read_access_and_default_values():
    try:
        config = serial_comm.load_config(r'..\config.toml')
    except FileNotFoundError:
        config = serial_comm.load_config(r'config.toml')
    ser = serial_comm.serial_init(config)
    default_values = {}
    default_values_exp = {}
    try:
        # get current values
        for register in config['direct_access_registers']:
            default_value_raw = serial_comm.read_registers(ser, len(register['address']), int(register['address'][0], 16))
            pattern = re.compile(r'[0-9]:[0-9]{2}:([0-9A-Fa-f]+)\r')
            default_value = re.search(pattern, default_value_raw)
            try:
                default_values[register['address'][0]] = int(default_value.group(1), 16)
                default_values_exp[register['address'][0]] = int(register['default_value'], 16)
            except ValueError:
                default_values[register['address'][0]] = None
                default_values_exp[register['address'][0]] = None
            time.sleep(0.1)
        # compare them to expected values
        assert default_values == default_values_exp
        # # spodnji test prikaže le prvi vrednosti, ki se razlikujeta, zgornji vse.
        # for address in default_values:
        #     assert default_values[address] == default_values_exp[address]
    finally:
        ser.close()
        print('Port closed')


def test_write_access():
    try:
        config = serial_comm.load_config(r'..\config.toml')
    except FileNotFoundError:
        config = serial_comm.load_config(r'config.toml')
    ser = serial_comm.serial_init(config)
    try:
        access = {}
        access_exp = {}
        for register in config['direct_access_registers']:
            if register['access'] == 'RW':
                out_raw = serial_comm.write_registers(ser, int(register['default_value']), int(register['address'][0], 16))
                out = out_raw.split('\r')[0]
                access_exp[register['address'][0]] = '0'
                access[register['address'][0]] = out
        assert access == access_exp
    finally:
        ser.close()
        print('Port closed')


