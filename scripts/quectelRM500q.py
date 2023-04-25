#!/usr/bin/env python3
import logging
import os
import argparse
import time
import csv
from datetime import datetime
from attila.atre import ATRuntimeEnvironment
from attila.exceptions import ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError


# Parse command-line arguments
parser = argparse.ArgumentParser(description='CLI tool for interacting with a Quectel modem')
parser.add_argument('-m', '--measure')
parser.add_argument('-d', '--device', default='/dev/ttyUSB2', help='serial device path')
parser.add_argument('-t', '--timeout', type=int, default=2, help='serial timeout in seconds')
parser.add_argument('-l', '--logdir', default='/home/dante/logs', help='logging directory')
parser.add_argument('-f', '--logfile', default='my_log_file.csv', help='name of the log file (should be .csv)')
parser.add_argument('-s', '--setup', action="store_true", help='choose full setup +logs or capture logs')
args = parser.parse_args()

# Check if the logfile has .csv extension or not
if not args.logfile.endswith('.csv'):
    if '.' in args.logfile:
        file_split = args.logfile.split('.')
        args.logfile = file_split[0] + '.csv'
    else:
        args.logfile += '.csv'
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
if len(response.full_response) == 0:
    print(f"Device path {args.device} is wrong")
    exit(1)
else:
   print(f"Device path {args.device} is OK")

# Create logger
#logger = logging.getLogger('my_logger')
#logger.setLevel(logging.INFO)

# Create file handler
#log_file = os.path.join(args.logdir, args.logfile)
#file_handler = logging.FileHandler(log_file)
#file_handler.setLevel(logging.INFO)

# Create formatter
#formatter = logging.Formatter('%(asctime)s - %(message)s')
#file_handler.setFormatter(formatter)

# Add file handler to logger
#logger.addHandler(file_handler)
dirpath = args.logdir
filename= os.path.basename(args.logfile)
path = dirpath + '/' + filename
response_dict={}
# Function to execute command and log response
def execute_command(command):
    response = atrunenv.exec(command)
    print(command)
    response_code = response.full_response[1].strip("'")
    print(response_code)
    return response

try:
  # Execute each AT command once and store the results in a variable
    csq_response = execute_command('AT+CSQ').full_response[1].strip("'").split(',')
    qrsrp_response = execute_command('AT+QRSRP').full_response[1].strip("'").split(',')
    qrsrq_response = execute_command('AT+QRSRQ').full_response[1].strip("'").split(',')
    qsinr_response = execute_command('AT+QSINR').full_response[1].strip("'").split(',')

    # Populate the dictionary with the results
    response_dict = {
        'Measurement' : args.measure,
        'Date': time.asctime(time.localtime()),
        'RSSI (dBm)': csq_response[0].split(':')[1],
        'PRX path RSRP value (dBm)': qrsrp_response[0].split(':')[1],
        'DRX path RSRP value (dBm)': qrsrp_response[1],
        'RX2 path RSRP value (dBm)': qrsrp_response[2],
        'RX3 path RSRP value (dBm)': qrsrp_response[3],
        'PRX path RSRQ value (dB)': qrsrq_response[0].split(':')[1],
        'DRC path RSRQ value (dB)': qrsrq_response[1],
        'RX2 path RSRQ value (dB)': qrsrq_response[2],
        'RX3 path RSRQ value (dB)': qrsrq_response[3],
        'PRX path SINR value (dB)': qsinr_response[0].split(':')[1],
        'DRX path SINR value (dB)': qsinr_response[1],
        'RX2 path SINR value (dB)': qsinr_response[2],
        'RX3 path SINR value (dB)': qsinr_response[3]
    }
    print(response_dict)

# Get the headers from the dictionary keys
    headers = response_dict.keys()

# Create the CSV file if it does not exist
    if not os.path.exists(path):
        log_file = os.path.join(args.logdir, args.logfile)
        with open(log_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)

# Write the dictionary values to the CSV file
    with open(path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writerow(response_dict)

# Check for error
except (ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError) as e:
    logger.error(f"An error occurred: {str(e)}")

# Close serial connection
atrunenv.close_serial()

