# -*- coding: utf-8 -*-

'''
Script:
    filesrw.py
Description:
    File system files functions
Author:
    Jose Miguel Rios Rubio
Date:
    01/01/2021
Version:
    1.0.0
'''

####################################################################################################

### Imported modules ###

from os import path as os_path
from os import remove as os_remove
from os import makedirs as os_makedirs
from os import utime as os_utime

from constants import LOG
from auxiliar import print_log, is_running_with_py3

####################################################################################################

### Files Functions ###

def create_parents_dirs(file_path):
    '''Create all parents directories from provided file path (mkdir -p $file_path).'''
    try:
        parentdirpath = os_path.dirname(file_path)
        if not os_path.exists(parentdirpath):
            os_makedirs(parentdirpath, 0o775)
    except Exception as e:
        print_log(LOG.ERROR, "Can't create parents directories of {}. {}".format(file_path, str(e)))


def file_exists(file_path=None):
    '''Check if the given file exists'''
    # Check if no path provided or file doesnt exists
    if file_path is None:
        return None
    if not os_path.exists(file_path):
        return False
    return True


def file_read_all_bin(file_path):
    '''Read all file content as binary and return it.'''
    # Check if no path provided or file doesnt exists
    if file_path is None:
        return None
    if not os_path.exists(file_path):
        print_log(LOG.ERROR, "File {} not found.".format(file_path))
        return None
    # File exists, so open and read it
    read = None
    try:
        with open(file_path, "rb") as f:
            read = f.read()
    except Exception as e:
        print_log(LOG.ERROR, "Can't open and read file {}. {}".format(file_path, str(e)))
    return read


def file_read_all_text(file_path):
    '''Read all text file content and return it in a string.'''
    read = ""
    # Check if file doesnt exists
    if not os_path.exists(file_path):
        print_log(LOG.ERROR, "File {} not found.".format(file_path))
    # File exists, so open and read it
    else:
        try:
            if is_running_with_py3():
                with open(file_path, "r", encoding="utf-8") as f:
                    read = f.read()
            else:
                with open(file_path, "r") as f:
                    read = f.read()
        except Exception as e:
            print_log(LOG.ERROR, "Can't open and read file {}. {}".format(file_path, str(e)))
    return read


def file_write(file_path, text=""):
    '''Write text to provided file.'''
    create_parents_dirs(file_path)
    # Determine if file exists and set open mode to write or append
    if not os_path.exists(file_path):
        print_log(LOG.INFO, "File {} not found, creating it...".format(file_path))
    # Try to Open and write to file
    if is_running_with_py3():
        try:
            with open(file_path, 'a', encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print_log(LOG.ERROR, "Can't write to file {}. {}".format(file_path, str(e)))
    else:
        try:
            with open(file_path, 'a') as f:
                f.write(text)
        except Exception as e:
            print_log(LOG.ERROR, "Can't write to file {}. {}".format(file_path, str(e)))


def file_write_line(file_path, text=""):
    '''Write a new line to provided file.'''
    create_parents_dirs(file_path)
    # Determine if file exists and set open mode to write or append
    if not os_path.exists(file_path):
        print_log(LOG.INFO, "File {} not found, creating it...".format(file_path))
    # Try to Open and write to file
    if is_running_with_py3():
        try:
            with open(file_path, 'a', encoding="utf-8") as f:
                f.write("{}\n".format(text))
        except Exception as e:
            print_log(LOG.ERROR, "Can't write to file {}. {}".format(file_path, str(e)))
    else:
        try:
            with open(file_path, 'a') as f:
                f.write("{}\n".format(text))
        except Exception as e:
            print_log(LOG.ERROR, "Can't write to file {}. {}".format(file_path, str(e)))


def file_clear(file_path):
    '''Remove and recreate a file to empty file content.'''
    create_parents_dirs(file_path)
    try:
        if os_path.exists(file_path):
            os_remove(file_path)
        with open(file_path, 'a'):
            os_utime(file_path, None)
    except Exception as e:
        print_log(LOG.ERROR, "Can't clear file {}. {}".format(file_path, str(e)))

