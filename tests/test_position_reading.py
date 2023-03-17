import pytest
import time
import re
import serial_comm


def test_crc_correct_format():
    config = serial_comm.load_config(r'config.toml')
    ser = serial_comm.serial_init(config)
    # TODO: ali je ta test sploh potreben?
    """ Tests correct CRC format """
    CRC_FORMAT_exp = '^C(([0-9]){2}:){3}[01]:[01]$'
    assert re.match(CRC_FORMAT_exp, config['encoder']['CRC_FORMAT']) is not None


def test_for_warning_error_flag():
    config = serial_comm.load_config(r'config.toml')
    ser = serial_comm.serial_init(config)
    try:
        for i in range(200):
            pos_crc = serial_comm.read_position_crc(ser, config['encoder']['CRC_FORMAT'].encode())
            try:
                error_flag = int(pos_crc.split(':')[3], 16)
                warning_flag = int(pos_crc.split(':')[4], 16)
                assert (error_flag, warning_flag) == (0, 0)
            except IndexError:
                pass
            time.sleep(0.1)
    finally:
        ser.close()
        print('Port closed')