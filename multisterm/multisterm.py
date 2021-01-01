#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    multisterm.py
Description:
    Multi-Serial-Terminal that allows to access and control a Serial Port
    through multiples instances.
Author:
    Jose Miguel Rios Rubio
Date:
    01/01/2021
Version:
    1.0.0
'''

###############################################################################
### Imported modules

import time
from sys import argv as sys_argv
from sys import exit as sys_exit
from argparse import ArgumentParser as argparse_ArgumentParser
from threading import Thread

from constants import RC, LOG, CONST
from texts import TEXT
from auxiliar import print_log, stdin_input
from serialcomm import (
    serial_open, serial_close, serial_read, serial_read_str, serial_write
)

###############################################################################
### Globals

ser = None
th_read = None
th_write = None
g_terminal_close = False

###############################################################################

def show_help():
    '''Print to stdout program usage help info.'''
    text_help = TEXT.HELP.format(
                    CONST.APP_VERSION, CONST.AUTHOR,
                    CONST.PROJECT_REPO, CONST.DEV_PAYPAL
                )
    print(LOG.INFO, text_help)


def parse_options():
    '''Get and parse program input arguments.'''
    arg_parser = argparse_ArgumentParser()
    arg_parser.version = CONST.APP_VERSION
    arg_parser.add_argument("-p", "--port", help=TEXT.OPT_PORT, 
                            action='store', nargs=1, type=str)
    arg_parser.add_argument("-b", "--bauds", help=TEXT.OPT_BAUDS,
                            action='store', nargs=1, type=int)
    arg_parser.add_argument("-l", "--log", help=TEXT.OPT_LOG,
                            action='store', nargs=1, type=str)
    arg_parser.add_argument("-v", "--version", action='version')
    args = arg_parser.parse_args()
    return vars(args)


def auto_detect_serial_bauds(serial_port):
    '''Automatic Serial baudrate detection (check for ascii text in commons
    bauds).'''
    bauds = 0
    ser = None
    for common_baud in CONST.SERIAL_COMMON_BAUDS:
        # Try to open Serial port at current common baud rate
        # If port can't be open, continue to next common bauds
        print("\nChecking {} bauds...".format(common_baud))
        ser = serial_open(serial_port, common_baud, 1.0, 1.0)
        if ser is None:
            continue
        time.sleep(2)
        # Send some strange string with end of line and read response
        serial_write(ser, CONST.SERIAL_AUTODETECT_BAUDS_SEND)
        readed_bytes = serial_read_str(ser)
        if len(readed_bytes) == 0:
            serial_close(ser)
            continue
        # Remove end of line bytes
        readed_bytes = readed_bytes.replace("\r", "")
        readed_bytes = readed_bytes.replace("\n", "")
        # Ignore if readed bytes are less than 10 characters
        if len(readed_bytes) < 5:
            serial_close(ser)
            continue
        # Check how many characters are commons in human texts
        num_human_chars = 0
        for character in readed_bytes:
            if character in CONST.SERIAL_AUTODETECT_ASCII_LIST:
                num_human_chars = num_human_chars + 1
        # If >=70% of the read string are common human text characters
        # Assume that this is the correct baud rate
        if ((num_human_chars / len(readed_bytes)) *100) >= 70:
            bauds = common_baud
            print_log(LOG.INFO, "Seems that BuadRate is {}".format(bauds))
            serial_close(ser)
            break
        serial_close(ser)
    return bauds


def serial_terminal(port, bauds):
    '''Handle a Serial Terminal.'''
    global ser
    global th_read, th_write
    # Opening Serial Port
    print("\nOpening port {} at {} bauds...".format(port, bauds))
    ser = serial_open(port, bauds, 1.0, 1.0)
    if (ser is None) or (not ser.isOpen()):
        print_log(LOG.INFO, "Can't open Serial port.")
        return False
    time.sleep(2)
    # Launching Serial read and write threads
    th_read = Thread(target=th_serial_read, args=(ser,))
    th_write = Thread(target=th_serial_write, args=(ser,))
    th_read.start()
    th_write.start()
    th_read.join()
    th_write.join()
    # Close Serial Port
    if (ser is not None) and ser.isOpen():
        serial_close(ser)
    return True


def th_serial_read(ser):
    '''Serial Terminal read and show thread.'''
    while not g_terminal_close:
        read_str = serial_read_str(ser)
        if len(read_str) > 0:
            print(read_str)


def th_serial_write(ser):
    '''Serial Terminal write thread.'''
    global g_terminal_close
    while not g_terminal_close:
        write_str = stdin_input()
        if write_str == "--quit--":
            g_terminal_close = True
            break
        serial_write(ser, write_str)


###############################################################################
### Main Function

def main(argc, argv):
    '''Main Function.'''
    # Check and parse program options from arguments
    options = parse_options()
    print(options)
    # Serial Port
    serial_port = ""
    if options["port"] is None:
        show_help()
        sys_exit(RC.OK)
    serial_port = options["port"][0]
    # Serial Bauds
    serial_bauds = 0
    if options["bauds"] is None:
        print_log(LOG.INFO, "BaudRate not provided, detecting...")
        serial_bauds = auto_detect_serial_bauds(serial_port)
        if serial_bauds == 0:
            print_log(LOG.INFO, "BaudRate detection fail.")
            sys_exit(RC.OK)
    else:
        serial_bauds = options["bauds"][0]
    # Serial log file
    serial_log = ""
    if options["log"] is not None:
        serial_log = options["log"][0]
    # Serial Terminal
    rc = serial_terminal(serial_port, serial_bauds)
    # Program end
    if not rc:
        program_exit(RC.FAIL)
    program_exit(RC.OK)

###############################################################################
### Exit Function

def program_exit(return_code):
    '''Finish function.'''
    global ser
    # Check if unexpected exit code provided and use RC.FAIL in that case
    if (return_code != RC.OK) and (return_code != RC.FAIL):
        return_code = RC.FAIL
    # Close and free any pending memory
    if (ser is not None) and ser.isOpen():
        serial_close(ser)
    # Exit
    print_log(LOG.DEBUG, "Program exit ({}).\n".format(return_code))
    sys_exit(return_code)

###############################################################################
### Main Script execution Check

if __name__ == "__main__":
    try:
        main(len(sys_argv), sys_argv)
    except KeyboardInterrupt:
        g_terminal_close = True
        th_read.join()
        th_write.join()
        program_exit(RC.OK)
