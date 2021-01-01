
# multisterm

Python Serial Terminal to access same port by multiple instances.

## Description

- You can launch the terminal more than one time with the same Serial Port, "opening" the same serial port twice or more...

- If you don't specify the Baud Rate speed of the port, the terminal will try to auto-detect the Baud Rate by opening the port with commons speeds, sending a dummy string and reading what receives from the port, if there is enough ASCII characters readed, it will asume that this is the correct Baud Rate.

## Installation

Install requeriments through pip:

```bash
python -m pip install -r requirements.txt
```

## Usage Examples

Check help:

```bash
python multisterm.py
python multisterm.py -h
```

Launch the terminal to access ttyUSB0 port at 115200 bauds:

```bash
python multisterm.py -p /dev/ttyUSB0 -b 115200
```

Launch the terminal to access ttyS3 port trying auto-detect bauds:

```bash
python multisterm.py -p /dev/ttyS3
```

## Help

```bash
NAME
    multiserialterm - Multi-Serial-Terminal 1.0.0 (13/12/2020)

SYNOPSIS
    python multiserialterm.py [--help] [--version] [-p <PORT>] [-b <BAUDS>] [-l <LOG_FILE>]

DESCRIPTION
    Multi-Serial-Terminal for multiple connections and communication through some specific Serial port. Let\'s say that it is a serial terminal to allow \"open\" and use the same Serial port multiples times at the same time.
OPTIONS
    -h, --help
        Shows help text (current information).

    -p --port
        Specify the Serial port to use.

    -b --bauds
        Specify Serial communication speed BaudRate.

    -l --log
        Specify a file to log all Serial received-transmitted data.

    -v, --version
        Shows current installed version.

AUTHOR
    Jose Miguel Rios Rubio

PROJECT REPOSITORY
    https://github.com/J-Rios/multiserialterm

DONATION
    Do you like this program, buy me a coffee:
    https://www.paypal.com/paypalme/josrios
```
