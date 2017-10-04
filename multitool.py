#!/usr/bin/python3.5
from distutils.util import strtobool
import socket
import threading
import argparse
import time

# Allows me to give y/n prompts
def yes_or_no(question):
    print('%s [y/n]' % question)
    while True:
        try:
            return strtobool(input('> '))
        except ValueError:
            print('Please give a valid yes or no.')

# Scans local ports, displays which are open
def port_scan():
    # Define dictionary for displaying ports and threads for speed
    port_dict = {}
    threads = []

    # Get user-given variables for connecting
    is_IP_known = yes_or_no('Do you know the IP of your scan target?')
    if is_IP_known == True:
        ip = input('What IP address would you like to scan?\n> ')
    else:
        try:
            ip = socket.gethostbyname(input('What is the web address you would like to scan?\n> '))
        except socket.gaierror:
            print('Hostname could not be resolved. Exiting program.')
    timeout = int(input('What should the timeout for connecting to a port be (in ms)?\n> '))

    print('Beginning to scan ports...')

    start_time = time.time()

    # Begin spawning of threads
    for i in range(10000):
        t = threading.Thread(target=TCP, args=(ip, i, timeout, port_dict))
        threads.append(t)

    # Start threading
    for i in range(10000):
        threads[i].start()

    # Allow threads to complete
    for i in range(10000):
        threads[i].join()

    # Display open ports
    for i in range(10000):
        if (port_dict[i]):
            print('# Listening on port %s' % str(i))

    # Determine time spent scanning
    print('Finished scan in %s seconds' % (round(time.time() - start_time, 2)))

# Connects to target IP and port with TCP
def TCP(ip, port, timeout, port_dict):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(timeout)
    try:
        sock.connect((ip, port))
        port_dict[port] = True
    except:
        port_dict[port] = False

# Define custom usage instructions
def usg(name=None):
    return '''multitool.py
    [scan - scans ports of given ip]
    '''

# Defines functions to be used with given command
FUNCTIONS = {
    'scan': port_scan
}

# Create parser to give program arguments and usage instructions in the terminal
parser = argparse.ArgumentParser(description='A simple, expandable netsec tool', usage=usg())
parser.add_argument('command', choices=FUNCTIONS.keys())

args = parser.parse_args()

# Execute user-given command
func = FUNCTIONS[args.command]
func()
