# -*- coding: utf-8 -*-

'''
Script:
    texts.py
Description:
    Multi-Serial-Terminal Texts
Author:
    Jose Miguel Rios Rubio
Date:
    01/01/2021
Version:
    1.0.0
'''

###############################################################################
### Texts

class TEXT():
    HELP = \
        "\n" \
        "NAME\n" \
        "       multiserialterm - Multi-Serial-Terminal {}\n" \
        "\n" \
        "SYNOPSIS\n" \
        "       python multiserialterm.py [--help] [--version] [-p <PORT>] " \
        "[-b <BAUDS>] [-l <LOG_FILE>]\n" \
        "\n" \
        "DESCRIPTION\n" \
        "       Multi-Serial-Terminal for multiple connections and " \
        "communication through some specific Serial port. Let's say that " \
        "it is a serial terminal to allow \"open\" and use the same Serial " \
        "port multiples times at the same time." \
        "\n" \
        "OPTIONS\n" \
        "       -h, --help\n" \
        "           Shows help text (current information).\n" \
        "\n" \
        "       -p --port\n" \
        "           Specify the Serial port to use.\n" \
        "\n" \
        "       -b --bauds\n" \
        "           Specify Serial communication speed BaudRate.\n" \
        "\n" \
        "       -l --log\n" \
        "           Specify a file to log all Serial received-transmitted data.\n" \
        "\n" \
        "       -v, --version\n" \
        "           Shows current installed version.\n" \
        "\n" \
        "AUTHOR\n" \
        "       {}\n" \
        "\n" \
        "PROJECT REPOSITORY" \
        "       {}\n" \
        "\n" \
        "DONATION\n" \
        "       Do you like this program, buy me a coffee:\n" \
        "       {}\n" \
        "\n"

    OPT_PORT = \
        "\n" \
        "Specify the Serial port to use"

    OPT_BAUDS = \
        "\n" \
        "Specify the Serial speed BaudRate"

    OPT_LOG = \
        "\n" \
        "Specify a file to log all Serial received-transmitted data"

    IGNORE_OPTION = \
        "\n" \
        "Ignoring unkown option \"{}\"."

    BAD_OPTION = \
        "\n" \
        "Invalid arguments provided. Check --help information about usage."

