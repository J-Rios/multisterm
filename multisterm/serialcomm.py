# -*- coding: utf-8 -*-

'''
Script:
    serialcomm.py
Description:
    Serial Port functions to ease communication.
Author:
    Jose Miguel Rios Rubio
Date:
    01/01/2021
Version:
    1.0.0
'''

###############################################################################
### Imported modules

from serial import Serial, SerialException, SerialTimeoutException, LF

from constants import LOG
from auxiliar import print_log, is_running_with_py3

###############################################################################
### Serial Functions

def serial_open(port, baudrate, read_timeout=None, write_timeout=None):
    '''Try to open a Serial Port.'''
    ser = None
    print_log(LOG.INFO, "Opening Serial port {} at {}bps...".format(
            port, str(baudrate)))
    try:
        ser = Serial(port=None)
        ser.port = port
        ser.baudrate = baudrate
        ser.timeout=read_timeout
        ser.write_timeout = write_timeout
        if not ser.isOpen():
            ser.open()
        ser.flush()
        print_log(LOG.INFO, "Port successfully open.")
    except Exception as e:
        print_log(LOG.ERROR, str(e))
    if (ser is None) or (not ser.isOpen()):
        ser = None
        print_log(LOG.ERROR, "Can't open serial port.")
    return ser


def serial_close(ser=None):
    '''Try to close a Serial Port.'''
    # Check if no port provided
    if ser is None:
        return
    port = ser.port
    print_log(LOG.INFO, "Closing Serial port {}...".format(port))
    try:
        ser.close()
        print_log(LOG.INFO, "Serial port {} closed.".format(port))
    except SerialException as e:
        print_log(LOG.ERROR, str(e))


def serial_read(ser=None, num_bytes=1024, timeout=None):
    '''Try to read from a Serial Port.'''
    # Check if no port provided
    if ser is None:
        return b''
    # Setup read timeout
    backup_timeout = ser.timeout
    if timeout is not None:
        ser.timeout = timeout
    # Read and restore default read timeout
    try:
        raw_read = ser.read(num_bytes)
    except Exception as e:
        print_log(LOG.ERROR, str(e))
    ser.timeout = backup_timeout
    print_log(LOG.DEBUG, "Serial read (bytes):\n{}".format(raw_read))
    if not raw_read:
        return b''
    return raw_read


def serial_read_str(ser=None, num_bytes=1024, timeout=None):
    '''Try to read from a Serial Port and return read data as string.'''
    raw_read = serial_read(ser, num_bytes, timeout)
    str_read = ""
    try:
        str_read = raw_read.decode()
    except Exception as e:
        print_log(LOG.ERROR, str(e))
    print_log(LOG.DEBUG, "Serial read (str):\n{}".format(str_read))
    return str_read


def serial_read_until(ser=None, expected=LF, num_bytes=1024, timeout=None):
    '''Try to read from a Serial Port until an expected bytes/substring.'''
    # Check if no port provided
    if ser is None:
        return ""
    # Setup read timeout
    backup_timeout = ser.timeout
    if timeout is not None:
        ser.timeout = timeout
    try:
        raw_read = ser.read_until(expected=expected, size=num_bytes)
    except Exception as e:
        print_log(LOG.ERROR, str(e))
    ser.timeout = backup_timeout
    print_log(LOG.DEBUG, "Serial read (bytes):\n{}".format(raw_read))
    # Parse to string
    str_read = ""
    try:
        str_read = str(raw_read) # str_read = raw_read.decode()
    except Exception as e:
        print_log(LOG.ERROR, str(e))
    print_log(LOG.DEBUG, "Serial read (str):\n{}".format(str_read))
    return str_read


def serial_write(ser=None, to_write=None):
    '''Basic Serial write function managed for Py2 and Py3 support.'''
    if ser is None:
        return None
    print_log(LOG.DEBUG, "Serial write (str):\n{}".format(to_write))
    if is_running_with_py3():
        to_write = to_write.encode()
    try:
        ser.write(to_write)
    except Exception as e:
        print_log(LOG.ERROR, str(e))
    print_log(LOG.DEBUG, "Serial write (bytes):\n{}".format(to_write))
    ser.flush()


def serial_flush(ser=None):
    '''Serial discard input buffer.'''
    if ser is None:
        return None
    ser.reset_input_buffer()
