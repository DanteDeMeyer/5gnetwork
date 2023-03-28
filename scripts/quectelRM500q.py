#!/usr/bin/env python3
import logging
import os
import argparse
import time
from datetime import datetime
from attila.atre import ATRuntimeEnvironment
from attila.exceptions import ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError


# Parse command-line arguments
parser = argparse.ArgumentParser(description='CLI tool for interacting with a Quectel modem')
parser.add_argument('-d', '--device', default='/dev/ttyUSB2', help='serial device path')
parser.add_argument('-t', '--timeout', type=int, default=2, help='serial timeout in seconds')
parser.add_argument('-l', '--logdir', default='/home/dante/logs', help='logging directory')
parser.add_argument('-f', '--logfile', default='my_log_file.txt', help='name of the log file')
args = parser.parse_args()

# Configuration
line_break = '\r\n'
baud_rate = 115200

# Check if log directory exists, create it if not
if not os.path.exists(args.logdir):
    os.makedirs(args.logdir)

# Create ATRuntimeEnvironment object
atrunenv = ATRuntimeEnvironment(True)

# Configure communicator
atrunenv.configure_communicator(args.device, baud_rate, args.timeout, line_break)

# Open serial port
atrunenv.open_serial()

# Check if device exists by sending an AT command and checking for an 'OK' response
response = atrunenv.exec('AT')
response_code = response.full_response[1].strip("'")
if response_code != 'OK':
    print(f"Device path {args.device} is wrong")
    atrunenv.close_serial()

# Create logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# Create file handler
log_file = os.path.join(args.logdir, args.logfile)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add file handler to logger
logger.addHandler(file_handler)


# Function to execute command and log response
def execute_command(command):
    response = atrunenv.exec(command)
    logger.info(f'{command}:')
    print(command)
    response_code = response.full_response[1].strip("'")
    print(response_code)
    return response

try:
    execute_command('AT+CIMI')
    execute_command('AT+cfun=0')
#    execute_command('AT+CGDCONT=1,"IPV4V6","oai"')
    time.sleep(3)
    execute_command('AT+cfun=1')
    time.sleep(10)
    execute_command('AT+CSQ')
    execute_command('AT+QRSRP')
    execute_command('AT+QRSRQ')
    execute_command('AT+QSINR')
    execute_command('AT+QNWCFG="nr5g_csi"')

 # Log the output of the specified AT commands
    #response = execute_command('AT+CSQ')
    logger.info('AT+CSQ:')
    logger.info(response.full_response)

    logger.info('AT+QRSRP:')
    logger.info(response.full_response)

    logger.info('AT+QRSRQ:')
    logger.info(response.full_response)

    logger.info('AT+QSINR:')
    logger.info(response.full_response)

    logger.info('AT+QNWCFG="nr5g_csi":')
    logger.info(response.full_response)

# Check for error
except (ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError) as e:
    logger.error(f"An error occurred: {str(e)}")

# Close serial connection
atrunenv.close_serial()

