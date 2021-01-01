# -*- coding: utf-8 -*-

'''
Script:
    auxiliar.py
Description:
    Auxiliar functions
Author:
    Jose Miguel Rios Rubio
Date:
    01/01/2021
Version:
    1.0.0
'''

###############################################################################
### Imported modules

from datetime import datetime as _datetime
from sys import stdout as sys_stdout
from sys import version_info as sys_version_info
from getpass import getpass

from constants import (
    LOG, CONST
)

###############################################################################
### Auxiliars Functions

def is_running_with_py2():
    '''Check if script is running using Python 2.'''
    if sys_version_info[0] == 2:
        return True
    return False


def is_running_with_py3():
    '''Check if script is running using Python 3.'''
    if sys_version_info[0] == 3:
        return True
    return False


def is_int(s, base=10):
    '''Check if provided string is an integer number.'''
    try:
        int(s, base)
        return True
    except ValueError:
        return False


def printts(to_print="", timestamp=True):
    '''printts with timestamp.'''
    print_without_ts = False
    # Normal print if timestamp is disabled
    if (not timestamp):
        print_without_ts = True
    else:
        # If to_print is text and not other thing
        if isinstance(to_print, str):
            # Normalize EOLs to new line
            to_print = to_print.replace("\r", "\n")
            # If no text provided or text just contain spaces or EOLs
            if to_print == "":
                print_without_ts = True
            elif (" " in to_print) and (len(set(to_print)) == 1):
                print_without_ts = True
            elif ("\n" in to_print) and (len(set(to_print)) == 1):
                print_without_ts = True
            else:
                # Normal print for all text start EOLs
                num_eol = -1
                for character in to_print:
                    if character == '\n':
                        print("")
                        num_eol = num_eol + 1
                    else:
                        break
                # Remove all text start EOLs (if any)
                if num_eol != -1:
                    to_print = to_print[num_eol+1:]
    if print_without_ts:
        print(to_print)
    else:
        # Get actual time and print with timestamp
        actual_date = _datetime.utcnow().strftime(CONST.LOG_TIMESTAMP_FORMAT)
        print("{} - {}".format(actual_date, to_print))


def print_log(log_level, log_text):
    '''Print according to a debug level.'''
    if CONST.LOG_LEVEL <= LOG.DEBUG:
        printts("[{}] {}".format(log_level_to_text(log_level), log_text))
        sys_stdout.flush()
    elif CONST.LOG_LEVEL == LOG.INFO:
        if log_level >= LOG.INFO:
            printts("[{}] {}".format(log_level_to_text(log_level), log_text))
            sys_stdout.flush()
    elif CONST.LOG_LEVEL == LOG.WARNING:
        if log_level >= LOG.WARNING:
            printts("[{}] {}".format(log_level_to_text(log_level), log_text))
            sys_stdout.flush()
    elif CONST.LOG_LEVEL == LOG.ERROR:
        if log_level >= LOG.ERROR:
            printts("[{}] {}".format(log_level_to_text(log_level), log_text))
            sys_stdout.flush()


def log_level_to_text(log_level):
    '''Convert log level number to string.'''
    if log_level <= LOG.DEBUG:
        return "DEBUG"
    elif log_level == LOG.INFO:
        return "INFO"
    elif log_level == LOG.WARNING:
        return "WARNING"
    elif log_level >= LOG.ERROR:
        return "ERROR"
    else:
        return "ERROR"


def stdin_input(text="", hide=True):
    '''Portable get standard input from keyboard.'''
    in_str = ""
    if hide:
        in_str = getpass(text)
    else:
        if is_running_with_py2():
            in_str = raw_input(text)
        else:
            in_str = input(text)
    return in_str
