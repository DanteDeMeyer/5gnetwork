#!/usr/bin/env python3
import argparse
import time
from datetime import datetime
from attila.atre import ATRuntimeEnvironment
from attila.exceptions import ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError


# Parse command-line arguments
parser = argparse.ArgumentParser(description='CLI tool for interacting with a Quectel modem')
parser.add_argument('-d', '--device', default='/dev/ttyUSB2', help='serial device path')
parser.add_argument('-t', '--timeout', type=int, default=2, help='serial timeout in seconds')
parser.add_argument('-s', '--setup', action="store_true", help='choose full setup +logs or capture logs')
args = parser.parse_args()

# Configuration
line_break = '\r\n'
baud_rate = 115200

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
# Function to execute command 
def execute_command(command):
    response = atrunenv.exec(command)
    print(command)
    response_code = response.full_response
    print(response_code)
    return response

try:
    if args.setup:
	print(time.asctime(time.localtime()))
        execute_command('AT+CIMI')
        execute_command('AT+cfun=0')
        time.sleep(3)
        execute_command('AT+cfun=1')
    else:
	print(time.asctime(time.localtime()))
        execute_command('AT+cfun=0')
        time.sleep(3)
        execute_command('AT+cfun=1')
        time.sleep(2)
        execute_command('AT+QMBNCFG="Select","ROW_Commercial"')
        execute_command('AT+QMBNCFG="AutoSel",0')
        execute_command('AT+CFUN=1,1')
        execute_command('AT+CGDCONT=2')
        execute_command('AT+CGDCONT=3')
	execute_command('AT+QNWPREFCFG= "nr5g_band",78')
	execute_command('AT+QNWPREFCFG= "mode_pref",NR5G')
	execute_command('AT+CGACT=1,1')
	execute_command('AT+CGPADDR=1')
	execute_command('AT+QSCAN')
	execute_command('AT+cfun=0')
        time.sleep(3)
        execute_command('AT+cfun=1')

# Check for error
except (ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError) as e:
    logger.error(f"An error occurred: {str(e)}")

# Close serial connection
atrunenv.close_serial()
